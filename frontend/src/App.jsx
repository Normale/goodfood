import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header/Header';
import MealInput from './components/MealInput/MealInput';
import MealsList from './components/MealsList/MealsList';
import DailyGoals from './components/DailyGoals/DailyGoals';
import TopNutrientGaps from './components/TopNutrientGaps/TopNutrientGaps';
import NextMealSuggestion from './components/NextMealSuggestion/NextMealSuggestion';
import NutrientAnalysis from './components/NutrientAnalysis/NutrientAnalysis';
import { DatabaseIcon, UserIcon, TargetIcon, ActivityIcon, CheckCircleIcon, SparklesIcon } from './components/ui/Icons';
import './App.css';

// Sample initial data
const initialMeals = [
  {
    id: 1,
    time: '8:30 AM',
    description: 'Oatmeal with berries, banana, and almond butter',
    calories: 420,
    protein: 12,
    carbs: 68,
    fat: 14
  },
  {
    id: 2,
    time: '12:45 PM',
    description: 'Grilled chicken salad with quinoa and avocado',
    calories: 580,
    protein: 42,
    carbs: 45,
    fat: 22
  },
  {
    id: 3,
    time: '3:15 PM',
    description: 'Greek yogurt with honey and walnuts',
    calories: 280,
    protein: 15,
    carbs: 32,
    fat: 11
  }
];

const initialGoals = [
  { name: 'Calories', current: 1450, target: 2000, unit: '' },
  { name: 'Protein', current: 65, target: 100, unit: 'g' },
  { name: 'Carbs', current: 210, target: 225, unit: 'g' },
  { name: 'Fat', current: 42, target: 65, unit: 'g' }
];

const initialSuggestion = {
  meal: 'Salmon with quinoa and roasted vegetables',
  reasoning: 'High in protein and omega-3s, adds fiber from quinoa and veggies'
};

const initialAnalysis = {
  deficient: [
    {
      name: 'Vitamin D',
      status: 'deficient',
      note: 'Consider adding fatty fish, egg yolks, or fortified foods'
    },
    {
      name: 'Fiber',
      status: 'deficient',
      note: 'Add more whole grains, fruits, and vegetables to your diet'
    }
  ],
  adequate: [
    {
      name: 'Protein',
      status: 'adequate',
      note: 'Meeting your daily protein requirements'
    },
    {
      name: 'Iron',
      status: 'adequate',
      note: 'Good iron levels from your current diet'
    }
  ],
  excessive: [
    {
      name: 'Sodium',
      status: 'excessive',
      note: 'Consider reducing processed foods and added salt'
    }
  ]
};

const initialNutrientData = {
  vitamin_d: 8,      // 8 out of 20 mcg = 40%
  fiber: 15,         // 15 out of 30 g = 50%
  iron: 12,          // 12 out of 18 mg = 67%
  calcium: 500,      // 500 out of 1000 mg = 50%
  vitamin_b12: 1.5,  // 1.5 out of 2.4 mcg = 62.5%
  omega_3: 0.8,      // 0.8 out of 1.6 g = 50%
};

function App() {
  const [meals, setMeals] = useState(initialMeals);
  const [goals, setGoals] = useState(initialGoals);
  const [suggestion, setSuggestion] = useState(initialSuggestion);
  const [analysis, setAnalysis] = useState(initialAnalysis);
  const [nutrientData, setNutrientData] = useState(initialNutrientData);
  const [activeTab, setActiveTab] = useState('tracker');

  // WebSocket connection
  const ws = useRef(null);
  const [isConnected, setIsConnected] = useState(false);

  // Personalization state
  const [userProfile, setUserProfile] = useState({
    age: '',
    gender: 'male',
    activityLevel: 'moderate',
    sleepQuality: 'good',
    stressLevel: 'moderate',
    healthConcerns: [],
    dietaryPreferences: ''
  });

  // Nutrient targets state
  const [nutrientTargets, setNutrientTargets] = useState({
    // Macronutrients
    carbohydrates: { value: 275, average: 250 },
    protein: { value: 110, average: 75 },
    totalFats: { value: 73, average: 65 },
    alphaLinolenicAcid: { value: 1.6, average: 1.6 },
    linoleicAcid: { value: 17, average: 14 },
    epaDha: { value: 250, average: 250 },
    solubleFiber: { value: 10, average: 10 },
    insolubleFiber: { value: 15, average: 15 },
    water: { value: 2500, average: 2000 },

    // Vitamins
    vitaminC: { value: 90, average: 90 },
    vitaminB1: { value: 1.2, average: 1.2 },
    vitaminB2: { value: 1.3, average: 1.3 },
    vitaminB3: { value: 16, average: 16 },
    vitaminB5: { value: 5, average: 5 },
    vitaminB6: { value: 1.7, average: 1.3 },
    vitaminB7: { value: 30, average: 30 },
    vitaminB9: { value: 400, average: 400 },
    vitaminB12: { value: 2.4, average: 2.4 },
    vitaminA: { value: 900, average: 900 },
    vitaminD: { value: 20, average: 15 },
    vitaminE: { value: 15, average: 15 },
    vitaminK: { value: 120, average: 90 },

    // Minerals
    calcium: { value: 1000, average: 1000 },
    phosphorus: { value: 700, average: 700 },
    magnesium: { value: 420, average: 320 },
    potassium: { value: 3500, average: 3400 },
    sodium: { value: 2300, average: 2300 },
    chloride: { value: 2300, average: 2300 },
    iron: { value: 18, average: 18 },
    zinc: { value: 11, average: 11 },
    copper: { value: 900, average: 900 },
    selenium: { value: 55, average: 55 },
    manganese: { value: 2.3, average: 2.3 },
    iodine: { value: 150, average: 150 },
    chromium: { value: 35, average: 35 },
    molybdenum: { value: 45, average: 45 },

    // Essential Amino Acids
    leucine: { value: 3, average: 2.73 },
    lysine: { value: 2.8, average: 2.1 },
    valine: { value: 1.9, average: 1.82 },
    isoleucine: { value: 1.5, average: 1.4 },
    threonine: { value: 1.3, average: 1.05 },
    methionine: { value: 1.2, average: 1.05 },
    phenylalanine: { value: 1.8, average: 1.75 },
    histidine: { value: 0.9, average: 0.7 },
    tryptophan: { value: 0.4, average: 0.28 },

    // Beneficial Compounds
    choline: { value: 550, average: 550 },
    taurine: { value: 200, average: 100 },
    coq10: { value: 100, average: 100 },
    alphaLipoicAcid: { value: 300, average: 300 }
  });

  // WebSocket setup - connect on mount
  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://localhost:8000/ws');

      ws.current.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
      };

      ws.current.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log('Received update:', message);

        // Route updates to appropriate components
        switch (message.component) {
          case 'todaysMeals':
            setMeals(message.data);
            // Recalculate goals based on new meals
            const totalCals = message.data.reduce((sum, meal) => sum + meal.calories, 0);
            const totalProt = message.data.reduce((sum, meal) => sum + meal.protein, 0);
            const totalCarbs = message.data.reduce((sum, meal) => sum + meal.carbs, 0);
            const totalFat = message.data.reduce((sum, meal) => sum + meal.fat, 0);

            setGoals([
              { name: 'Calories', current: totalCals, target: 2000, unit: '' },
              { name: 'Protein', current: totalProt, target: 100, unit: 'g' },
              { name: 'Carbs', current: totalCarbs, target: 225, unit: 'g' },
              { name: 'Fat', current: totalFat, target: 65, unit: 'g' }
            ]);
            break;

          case 'nutrientGaps':
            setNutrientData(message.data);
            break;

          case 'recommendedMeal':
            setSuggestion(message.data);
            break;

          default:
            console.warn('Unknown component:', message.component);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      ws.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
    };

    connectWebSocket();

    // Cleanup on unmount
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  // Calculate total calories and protein
  const totalCalories = meals.reduce((sum, meal) => sum + meal.calories, 0);
  const totalProtein = meals.reduce((sum, meal) => sum + meal.protein, 0);

  const handleMealSubmit = async (mealText) => {
    if (!isConnected) {
      console.error('WebSocket not connected');
      return;
    }

    // Send message to backend via WebSocket
    ws.current.send(JSON.stringify({
      action: 'add_meal',
      text: mealText
    }));

    // The backend will broadcast updates to all clients
    // No need to update state here - wait for WebSocket message
  };

  const handleDeleteMeal = (mealId) => {
    const mealToDelete = meals.find(m => m.id === mealId);
    if (mealToDelete) {
      setMeals(meals.filter(m => m.id !== mealId));

      // Update goals
      setGoals(goals.map(goal => {
        const decreases = {
          'Calories': mealToDelete.calories,
          'Protein': mealToDelete.protein,
          'Carbs': mealToDelete.carbs,
          'Fat': mealToDelete.fat
        };
        return {
          ...goal,
          current: Math.max(0, goal.current - (decreases[goal.name] || 0))
        };
      }));
    }
  };

  const handleThemeToggle = () => {
    console.log('Theme toggled');
  };

  return (
    <div className="app">
      <Header
        totalCalories={totalCalories}
        totalProtein={totalProtein}
        onThemeToggle={handleThemeToggle}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      <div className="main-container">
        {activeTab === 'tracker' && (
          <div className="content-grid">
            <div className="left-column">
              <MealInput onSubmit={handleMealSubmit} />
              <MealsList meals={meals} onDeleteMeal={handleDeleteMeal} />
            </div>

            <div className="right-column">
              {/* <DailyGoals goals={goals} /> */}
              <TopNutrientGaps nutrientData={nutrientData} />
              <NextMealSuggestion suggestion={suggestion} />
              <NutrientAnalysis analysis={analysis} />
            </div>
          </div>
        )}

        {activeTab === 'database' && (
          <motion.div
            key="database"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
            style={{ padding: '1.5rem' }}
          >
            {/* Food Explorer */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                  <DatabaseIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Browse Foods</h3>
                  <p className="text-sm text-white/60">Complete nutrient profiles</p>
                </div>
              </div>

              <div className="space-y-3">
                {[
                  { name: 'Salmon (Atlantic, wild)', category: 'Fish & Seafood', protein: 25.4, carbs: 0, fats: 13.4, highlight: 'EPA+DHA: 2260mg' },
                  { name: 'Spinach (raw)', category: 'Vegetables', protein: 2.9, carbs: 3.6, fats: 0.4, highlight: 'Vitamin K: 483mcg' },
                  { name: 'Almonds (raw)', category: 'Nuts & Seeds', protein: 21.2, carbs: 21.6, fats: 49.9, highlight: 'Vitamin E: 25.6mg' },
                  { name: 'Blueberries (fresh)', category: 'Fruits', protein: 0.7, carbs: 14.5, fats: 0.3, highlight: 'Polyphenols: 560mg' },
                  { name: 'Eggs (whole, large)', category: 'Protein Sources', protein: 6.3, carbs: 0.6, fats: 5.3, highlight: 'Choline: 147mg' },
                ].map((food, index) => (
                  <motion.div
                    key={food.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="font-medium text-white">{food.name}</h4>
                        <p className="text-xs text-white/50">{food.category}</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-2 text-xs mb-2">
                      <div>
                        <p className="text-white/50">Protein</p>
                        <p className="text-white font-medium">{food.protein}g</p>
                      </div>
                      <div>
                        <p className="text-white/50">Carbs</p>
                        <p className="text-white font-medium">{food.carbs}g</p>
                      </div>
                      <div>
                        <p className="text-white/50">Fats</p>
                        <p className="text-white font-medium">{food.fats}g</p>
                      </div>
                    </div>
                    <div className="pt-2 border-t border-white/10">
                      <p className="text-xs text-cyan-400">{food.highlight}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Add Food Form */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                  <DatabaseIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Add to Database</h3>
                  <p className="text-sm text-white/60">Expand your food library</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white/70 mb-2">Food Name</label>
                  <input
                    type="text"
                    placeholder="e.g., Grilled Chicken Breast"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-white/70 mb-2">Category</label>
                  <select className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50">
                    <option>Protein Sources</option>
                    <option>Vegetables</option>
                    <option>Fruits</option>
                    <option>Nuts & Seeds</option>
                    <option>Fish & Seafood</option>
                  </select>
                </div>

                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Protein (g)</label>
                    <input
                      type="number"
                      placeholder="0"
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Carbs (g)</label>
                    <input
                      type="number"
                      placeholder="0"
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Fats (g)</label>
                    <input
                      type="number"
                      placeholder="0"
                      className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-white/70 mb-2">Key Nutrients</label>
                  <textarea
                    placeholder="e.g., Vitamin B12: 2.5mcg, Iron: 1.2mg"
                    rows={3}
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50 resize-none"
                  />
                </div>

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 text-white font-medium shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all"
                >
                  Add to Database
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'personalization' && (
          <motion.div
            key="personalization"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-6"
            style={{ padding: '1.5rem' }}
          >
            {/* Profile & Lifestyle */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center">
                  <UserIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Profile & Lifestyle</h3>
                  <p className="text-sm text-white/60">Help us personalize your experience</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Age</label>
                    <input
                      type="number"
                      placeholder="e.g., 32"
                      value={userProfile.age}
                      onChange={(e) => setUserProfile({ ...userProfile, age: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Gender</label>
                    <select
                      value={userProfile.gender}
                      onChange={(e) => setUserProfile({ ...userProfile, gender: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    >
                      <option value="male">Male</option>
                      <option value="female">Female</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-white/70 mb-2">Activity Level</label>
                  <select
                    value={userProfile.activityLevel}
                    onChange={(e) => setUserProfile({ ...userProfile, activityLevel: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                  >
                    <option value="sedentary">Sedentary (desk job, minimal movement)</option>
                    <option value="light">Lightly Active (1-3 days exercise)</option>
                    <option value="moderate">Moderately Active (3-5 days exercise)</option>
                    <option value="active">Very Active (6-7 days exercise)</option>
                    <option value="athlete">Athlete (intense daily training)</option>
                  </select>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Sleep Quality</label>
                    <select
                      value={userProfile.sleepQuality}
                      onChange={(e) => setUserProfile({ ...userProfile, sleepQuality: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    >
                      <option value="poor">Poor (4-5 hours)</option>
                      <option value="fair">Fair (5-6 hours)</option>
                      <option value="good">Good (7-8 hours)</option>
                      <option value="excellent">Excellent (8+ hours)</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Stress Level</label>
                    <select
                      value={userProfile.stressLevel}
                      onChange={(e) => setUserProfile({ ...userProfile, stressLevel: e.target.value })}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                    >
                      <option value="low">Low</option>
                      <option value="moderate">Moderate</option>
                      <option value="high">High</option>
                      <option value="very_high">Very High</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-white/70 mb-2">Dietary Preferences</label>
                  <textarea
                    placeholder="e.g., Vegetarian, pescatarian, paleo, no processed foods..."
                    rows={3}
                    value={userProfile.dietaryPreferences}
                    onChange={(e) => setUserProfile({ ...userProfile, dietaryPreferences: e.target.value })}
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none"
                  />
                </div>
              </div>
            </div>

            {/* Health Concerns & Goals */}
            <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                  <SparklesIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Health Concerns & Goals</h3>
                  <p className="text-sm text-white/60">What would you like to optimize?</p>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-white/70 mb-3">Select your health focus areas:</label>
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      {
                        id: 'hair',
                        label: 'Hair Health',
                        desc: 'Biotin, zinc, and iron support keratin synthesis and follicle function. Methionine provides sulfur for hair structure.'
                      },
                      {
                        id: 'skin',
                        label: 'Skin Health',
                        desc: 'Vitamin C for collagen synthesis, EPA+DHA for inflammation, vitamin E and selenium for antioxidant protection.'
                      },
                      {
                        id: 'eyes',
                        label: 'Eye Health',
                        desc: 'Vitamin A for rhodopsin production, EPA+DHA for retinal structure, zinc for vitamin A transport and macular health.'
                      },
                      {
                        id: 'cognitive',
                        label: 'Cognitive Function',
                        desc: 'EPA+DHA enhance neuroplasticity, B vitamins support neurotransmitter synthesis, choline for acetylcholine production.'
                      },
                      {
                        id: 'energy',
                        label: 'Energy & Vitality',
                        desc: 'B vitamins as cofactors in energy metabolism, iron for oxygen transport, magnesium and CoQ10 for ATP production.'
                      },
                      {
                        id: 'immune',
                        label: 'Immune System',
                        desc: 'Vitamin C and D regulate immune cells, zinc for T-cell development, selenium for antioxidant defense.'
                      },
                      {
                        id: 'heart',
                        label: 'Heart Health',
                        desc: 'EPA+DHA reduce triglycerides, magnesium regulates vascular tone, soluble fiber lowers LDL cholesterol.'
                      },
                      {
                        id: 'gut',
                        label: 'Gut Health',
                        desc: 'Fiber feeds microbiome and supports motility, zinc maintains intestinal barrier, vitamin A for mucosal immunity.'
                      },
                      {
                        id: 'bone',
                        label: 'Bone Health',
                        desc: 'Calcium and phosphorus for mineralization, vitamin D for absorption, vitamin K activates osteocalcin.'
                      },
                      {
                        id: 'joint',
                        label: 'Joint Health',
                        desc: 'Vitamin C and copper for collagen synthesis, EPA+DHA reduce inflammation, manganese supports cartilage.'
                      },
                      {
                        id: 'mood',
                        label: 'Mood & Mental Health',
                        desc: 'EPA+DHA modulate neurotransmitters, B6/B9/B12 for serotonin synthesis, magnesium regulates stress response.'
                      },
                      {
                        id: 'longevity',
                        label: 'Longevity',
                        desc: 'Antioxidants (C, E, selenium) reduce oxidative stress, EPA+DHA preserve telomeres, fiber improves metabolic health.'
                      }
                    ].map(concern => (
                      <div key={concern.id} className="relative group">
                        <label className={`flex items-center gap-3 p-4 rounded-xl cursor-pointer transition-all duration-200 ${
                          userProfile.healthConcerns.includes(concern.id)
                            ? 'bg-gradient-to-r from-purple-500/20 to-pink-600/20 border-2 border-purple-500/50 shadow-lg shadow-purple-500/20'
                            : 'bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20'
                        }`}>
                          <div className="relative flex-shrink-0">
                            <input
                              type="checkbox"
                              checked={userProfile.healthConcerns.includes(concern.id)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setUserProfile({
                                    ...userProfile,
                                    healthConcerns: [...userProfile.healthConcerns, concern.id]
                                  });
                                } else {
                                  setUserProfile({
                                    ...userProfile,
                                    healthConcerns: userProfile.healthConcerns.filter(c => c !== concern.id)
                                  });
                                }
                              }}
                              className="w-5 h-5 rounded-md bg-white/10 border-white/20"
                            />
                          </div>
                          <span className="text-sm font-medium text-white">{concern.label}</span>
                        </label>
                        <div className="tooltip">
                          <div className="tooltip-arrow"></div>
                          <p className="text-xs text-white/90 leading-relaxed">{concern.desc}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {userProfile.healthConcerns.length > 0 && (
                  <div className="p-4 rounded-xl bg-gradient-to-r from-purple-500/10 to-pink-600/10 border border-purple-500/20">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircleIcon className="w-5 h-5 text-purple-400" />
                      <h4 className="text-sm font-semibold text-white">Personalized Recommendations</h4>
                    </div>
                    <p className="text-xs text-white/60">
                      Based on your selected focus areas, we'll highlight nutrients and foods that support {userProfile.healthConcerns.length} health goal{userProfile.healthConcerns.length > 1 ? 's' : ''}.
                    </p>
                  </div>
                )}

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 text-white font-medium shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all"
                >
                  Save Profile & Get Recommendations
                </motion.button>
              </div>
            </div>
          </motion.div>
        )}

        {activeTab === 'personalization' && (
          <motion.div
            key="nutrient-targets"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ delay: 0.2 }}
            className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6"
            style={{ margin: '1.5rem', marginTop: '0' }}
          >
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                  <TargetIcon className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white">Daily Nutrient Targets</h3>
                  <p className="text-sm text-white/60">Customize your daily nutrition goals</p>
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-2 rounded-lg bg-gradient-to-r from-emerald-500 to-teal-600 text-white text-sm font-medium shadow-lg shadow-emerald-500/30 hover:shadow-emerald-500/50 transition-all"
              >
                Save Targets
              </motion.button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(nutrientTargets).map(([key, data]) => {
                const diff = ((data.value - data.average) / data.average * 100).toFixed(0);
                const isHigher = data.value > data.average;
                const isEqual = data.value === data.average;

                const labels = {
                  // Macronutrients
                  carbohydrates: { name: 'Carbohydrates', unit: 'g' },
                  protein: { name: 'Protein', unit: 'g' },
                  totalFats: { name: 'Total Fats', unit: 'g' },
                  alphaLinolenicAcid: { name: 'Alpha-linolenic acid', unit: 'g' },
                  linoleicAcid: { name: 'Linoleic acid', unit: 'g' },
                  epaDha: { name: 'EPA+DHA', unit: 'mg' },
                  solubleFiber: { name: 'Soluble Fiber', unit: 'g' },
                  insolubleFiber: { name: 'Insoluble Fiber', unit: 'g' },
                  water: { name: 'Water', unit: 'ml' },

                  // Vitamins
                  vitaminC: { name: 'Vitamin C', unit: 'mg' },
                  vitaminB1: { name: 'Vitamin B1 Thiamine', unit: 'mg' },
                  vitaminB2: { name: 'Vitamin B2 Riboflavin', unit: 'mg' },
                  vitaminB3: { name: 'Vitamin B3 Niacin', unit: 'mg' },
                  vitaminB5: { name: 'Vitamin B5 Pantothenic acid', unit: 'mg' },
                  vitaminB6: { name: 'Vitamin B6 Pyridoxine', unit: 'mg' },
                  vitaminB7: { name: 'Vitamin B7 Biotin', unit: 'mcg' },
                  vitaminB9: { name: 'Vitamin B9 Folate', unit: 'mcg DFE' },
                  vitaminB12: { name: 'Vitamin B12', unit: 'mcg' },
                  vitaminA: { name: 'Vitamin A', unit: 'mcg RAE' },
                  vitaminD: { name: 'Vitamin D', unit: 'mcg' },
                  vitaminE: { name: 'Vitamin E', unit: 'mg' },
                  vitaminK: { name: 'Vitamin K', unit: 'mcg' },

                  // Minerals
                  calcium: { name: 'Calcium', unit: 'mg' },
                  phosphorus: { name: 'Phosphorus', unit: 'mg' },
                  magnesium: { name: 'Magnesium', unit: 'mg' },
                  potassium: { name: 'Potassium', unit: 'mg' },
                  sodium: { name: 'Sodium', unit: 'mg' },
                  chloride: { name: 'Chloride', unit: 'mg' },
                  iron: { name: 'Iron', unit: 'mg' },
                  zinc: { name: 'Zinc', unit: 'mg' },
                  copper: { name: 'Copper', unit: 'mcg' },
                  selenium: { name: 'Selenium', unit: 'mcg' },
                  manganese: { name: 'Manganese', unit: 'mg' },
                  iodine: { name: 'Iodine', unit: 'mcg' },
                  chromium: { name: 'Chromium', unit: 'mcg' },
                  molybdenum: { name: 'Molybdenum', unit: 'mcg' },

                  // Essential Amino Acids
                  leucine: { name: 'Leucine', unit: 'g' },
                  lysine: { name: 'Lysine', unit: 'g' },
                  valine: { name: 'Valine', unit: 'g' },
                  isoleucine: { name: 'Isoleucine', unit: 'g' },
                  threonine: { name: 'Threonine', unit: 'g' },
                  methionine: { name: 'Methionine', unit: 'g' },
                  phenylalanine: { name: 'Phenylalanine', unit: 'g' },
                  histidine: { name: 'Histidine', unit: 'g' },
                  tryptophan: { name: 'Tryptophan', unit: 'g' },

                  // Beneficial Compounds
                  choline: { name: 'Choline', unit: 'mg' },
                  taurine: { name: 'Taurine', unit: 'mg' },
                  coq10: { name: 'CoQ10', unit: 'mg' },
                  alphaLipoicAcid: { name: 'Alpha-lipoic acid', unit: 'mg' }
                };

                return (
                  <div key={key} className="p-4 rounded-xl bg-white/5 border border-white/10">
                    <div className="flex justify-between items-start mb-2">
                      <label className="text-sm font-medium text-white">{labels[key].name}</label>
                      {!isEqual && (
                        <span className={`text-xs px-2 py-1 rounded ${
                          isHigher
                            ? 'bg-emerald-500/20 text-emerald-400'
                            : 'bg-orange-500/20 text-orange-400'
                        }`}>
                          {isHigher ? '+' : ''}{diff}%
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        step="any"
                        value={data.value}
                        onChange={(e) => setNutrientTargets({
                          ...nutrientTargets,
                          [key]: { ...data, value: parseFloat(e.target.value) || 0 }
                        })}
                        className="flex-1 px-3 py-2 rounded-lg bg-white/10 border border-white/10 text-white text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/50"
                      />
                      <span className="text-xs text-white/50">{labels[key].unit}</span>
                    </div>
                    <p className="text-xs text-white/40 mt-2">Avg: {data.average} {labels[key].unit}</p>
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;
