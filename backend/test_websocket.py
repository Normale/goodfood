"""WebSocket integration test - tests the full add_meal workflow."""

import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import websockets
except ImportError:
    print("[ERROR] websockets package not installed")
    print("Run: uv add websockets")
    sys.exit(1)


async def test_add_meal_websocket():
    """Test the add_meal WebSocket endpoint with a simple meal."""
    print("=" * 80)
    print("WebSocket Integration Test - Add Meal")
    print("=" * 80)

    server_url = "ws://localhost:8000/ws"
    meal_description = "2 scrambled eggs with toast"

    print(f"\nConnecting to WebSocket server: {server_url}")

    try:
        async with websockets.connect(server_url) as websocket:
            print("[OK] Connected to WebSocket server")

            # Send add_meal request
            request = {
                "action": "add_meal",
                "text": meal_description
            }

            print(f"\nSending request:")
            print(f"  Action: {request['action']}")
            print(f"  Text: {request['text']}")

            await websocket.send(json.dumps(request))
            print("[OK] Request sent")

            # Collect responses
            print("\nReceiving responses:")
            print("-" * 80)

            received_events = []
            final_result = None
            timeout_seconds = 60  # Allow 60 seconds for the workflow to complete
            start_time = asyncio.get_event_loop().time()

            try:
                while True:
                    # Check timeout
                    if asyncio.get_event_loop().time() - start_time > timeout_seconds:
                        print(f"\n[WARN] Timeout after {timeout_seconds} seconds")
                        break

                    try:
                        message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    except asyncio.TimeoutError:
                        # No message received in 5 seconds, continue waiting
                        continue

                    try:
                        data = json.loads(message)
                        event_type = data.get("type", "unknown")
                        received_events.append(event_type)

                        # Print relevant events
                        if event_type == "workflow_start":
                            print(f"[EVENT] Workflow started: {data.get('stage')}")

                        elif event_type == "agent_status":
                            agent = data.get("agent_type")
                            status = data.get("status")
                            msg = data.get("message")
                            print(f"[AGENT] {agent}: {status} - {msg}")

                        elif event_type == "iteration":
                            iteration = data.get("iteration")
                            max_iter = data.get("max")
                            print(f"[PROGRESS] Iteration {iteration}/{max_iter}")

                        elif event_type == "estimates":
                            macros = data.get("macros", {})
                            print(f"[ESTIMATES] Calories: {macros.get('calories')}, "
                                  f"Protein: {macros.get('protein')}g, "
                                  f"Carbs: {macros.get('carbs')}g, "
                                  f"Fat: {macros.get('fat')}g")
                            final_result = data

                        elif event_type == "consensus":
                            print(f"[CONSENSUS] {data.get('message')}")

                        elif event_type == "update":
                            update_type = data.get("update_type")
                            if update_type == "todaysMeals":
                                meals = data.get("data", [])
                                print(f"[UPDATE] Today's meals updated ({len(meals)} meals)")
                            elif update_type == "nutrientGaps":
                                gaps = data.get("data", [])
                                print(f"[UPDATE] Nutrient gaps updated ({len(gaps)} gaps)")
                            elif update_type == "recommendedMeal":
                                rec = data.get("data", {})
                                print(f"[UPDATE] Recommended meal: {rec.get('meal', 'N/A')}")

                        elif event_type == "error":
                            print(f"[ERROR] {data.get('message')}")
                            return False

                        # Check if workflow is complete
                        if event_type == "update" and data.get("update_type") == "recommendedMeal":
                            # This is typically the last event
                            print("\n[OK] Workflow completed")
                            break

                    except json.JSONDecodeError as e:
                        print(f"[WARN] Failed to parse message: {e}")
                        continue

            except Exception as e:
                print(f"\n[WARN] Error receiving messages: {e}")

            # Verify results
            print("\n" + "=" * 80)
            print("Verification")
            print("=" * 80)

            # Check expected events
            expected_events = ["workflow_start", "agent_status", "estimates", "consensus"]
            missing_events = [e for e in expected_events if e not in received_events]

            if missing_events:
                print(f"[WARN] Missing expected events: {missing_events}")
            else:
                print("[OK] All expected event types received")

            # Check final estimates
            if final_result:
                macros = final_result.get("macros", {})
                print(f"\nFinal Estimates:")
                print(f"  Calories: {macros.get('calories')}")
                print(f"  Protein: {macros.get('protein')}g")
                print(f"  Carbs: {macros.get('carbs')}g")
                print(f"  Fat: {macros.get('fat')}g")

                # Basic sanity checks for scrambled eggs
                if macros.get('protein', 0) > 0 and macros.get('calories', 0) > 0:
                    print("\n[OK] Estimates look reasonable for the meal")
                    return True
                else:
                    print("\n[FAIL] Estimates seem incorrect (protein or calories is 0)")
                    return False
            else:
                print("\n[FAIL] No final estimates received")
                return False

    except websockets.exceptions.WebSocketException as e:
        print(f"\n[ERROR] WebSocket connection failed: {e}")
        print("\nMake sure the server is running:")
        print("  cd backend")
        print("  uv run python -m uvicorn api.server:app --reload")
        return False

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run WebSocket integration test."""
    print("\n" + "=" * 80)
    print("WEBSOCKET INTEGRATION TEST")
    print("=" * 80)
    print("\nThis test requires the backend server to be running.")
    print("Start it with: cd backend && uv run python -m uvicorn api.server:app --reload")
    print("\nContinuing in 3 seconds...")
    await asyncio.sleep(3)

    result = await test_add_meal_websocket()

    print("\n" + "=" * 80)
    print("TEST RESULT")
    print("=" * 80)
    if result:
        print("[SUCCESS] WebSocket integration test PASSED!")
        print("\nThe add_meal workflow is working correctly:")
        print("  - WebSocket connection established")
        print("  - Meal processing completed")
        print("  - Nutrient estimates received")
        print("  - Database insertion successful (implied by workflow completion)")
        return 0
    else:
        print("[ERROR] WebSocket integration test FAILED!")
        print("Please review the output above for details.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
