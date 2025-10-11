import { useState } from 'react';
import Header from './components/Header/Header';
import MealInput from './components/MealInput/MealInput';
import MealsList from './components/MealsList/MealsList';
import DailyGoals from './components/DailyGoals/DailyGoals';
import NextMealSuggestion from './components/NextMealSuggestion/NextMealSuggestion';
import NutrientAnalysis from './components/NutrientAnalysis/NutrientAnalysis';
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

function App() {
  const [meals, setMeals] = useState(initialMeals);
  const [goals, setGoals] = useState(initialGoals);
  const [suggestion, setSuggestion] = useState(initialSuggestion);
  const [analysis, setAnalysis] = useState(initialAnalysis);

  // Calculate total calories and protein
  const totalCalories = meals.reduce((sum, meal) => sum + meal.calories, 0);
  const totalProtein = meals.reduce((sum, meal) => sum + meal.protein, 0);

  const handleMealSubmit = async (mealText) => {
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // For demo purposes, just add a sample meal
    const newMeal = {
      id: Date.now(),
      time: new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' }),
      description: mealText,
      calories: 350,
      protein: 25,
      carbs: 40,
      fat: 12
    };

    setMeals([...meals, newMeal]);

    // Update goals
    setGoals(goals.map(goal => {
      const updates = {
        'Calories': 350,
        'Protein': 25,
        'Carbs': 40,
        'Fat': 12
      };
      return {
        ...goal,
        current: goal.current + (updates[goal.name] || 0)
      };
    }));
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
      />

      <div className="main-container">
        <div className="content-grid">
          <div className="left-column">
            <MealInput onSubmit={handleMealSubmit} />
            <MealsList meals={meals} onDeleteMeal={handleDeleteMeal} />
          </div>

          <div className="right-column">
            <DailyGoals goals={goals} />
            <NextMealSuggestion suggestion={suggestion} />
            <NutrientAnalysis analysis={analysis} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
