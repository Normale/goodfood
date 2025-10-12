import { useState } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header/Header';
import MealInput from './components/MealInput/MealInput';
import MealsList from './components/MealsList/MealsList';
import DailyGoals from './components/DailyGoals/DailyGoals';
import TopNutrientGaps from './components/TopNutrientGaps/TopNutrientGaps';
import NextMealSuggestion from './components/NextMealSuggestion/NextMealSuggestion';
import NutrientAnalysis from './components/NutrientAnalysis/NutrientAnalysis';
import { DatabaseIcon } from './components/ui/Icons';
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
              <NextMealSuggestion />
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
      </div>
    </div>
  );
}

export default App;
