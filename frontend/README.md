# NutriTrack AI Frontend

A modern, beautiful React-based nutrition tracking application with a dark gradient theme.

## Features

- **Meal Input**: AI-powered meal logging with real-time analysis
- **Today's Meals**: View all logged meals with detailed nutrition breakdown
- **Daily Goals**: Track progress toward calorie, protein, carbs, and fat goals
- **Next Meal Suggestion**: AI-generated recommendations based on current intake
- **Nutrient Analysis**: Comprehensive breakdown of deficient, adequate, and excessive nutrients

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header/
│   │   │   ├── Header.jsx
│   │   │   └── Header.css
│   │   ├── MealInput/
│   │   │   ├── MealInput.jsx
│   │   │   └── MealInput.css
│   │   ├── MealsList/
│   │   │   ├── MealsList.jsx
│   │   │   └── MealsList.css
│   │   ├── DailyGoals/
│   │   │   ├── DailyGoals.jsx
│   │   │   └── DailyGoals.css
│   │   ├── NextMealSuggestion/
│   │   │   ├── NextMealSuggestion.jsx
│   │   │   └── NextMealSuggestion.css
│   │   ├── NutrientAnalysis/
│   │   │   ├── NutrientAnalysis.jsx
│   │   │   └── NutrientAnalysis.css
│   │   └── ui/
│   │       └── Icons.jsx
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── package.json
└── vite.config.js
```

## Getting Started

### Install Dependencies
```bash
npm install
```

### Run Development Server
```bash
npm run dev
```

### Build for Production
```bash
npm run build
```

## Component Overview

### Header
- Displays app branding and logo
- Shows real-time calorie and protein totals
- Includes theme toggle button

### MealInput
- Text area for meal description
- AI-powered analysis with loading state
- Animated submit button with sparkles icon

### MealsList
- Scrollable list of today's meals
- Each meal card shows time, description, and macros
- Delete button on hover
- Empty state when no meals logged

### DailyGoals
- Progress bars for Calories, Protein, Carbs, Fat
- Color-coded status badges (On track / High)
- Animated progress fill with shimmer effect
- Shows percentage and remaining amounts

### NextMealSuggestion
- AI-generated meal recommendation
- Explains reasoning based on current intake
- Pulsing indicator for active suggestions
- Gradient border accent

### NutrientAnalysis
- Three sections: Needs Attention, On Track, Watch Out
- Color-coded by status (red/green/orange)
- Glow effects on hover
- Detailed recommendations for each nutrient

## Design Features

- **Dark gradient background**: Smooth gradient from dark blue to midnight
- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Animations**: Fade-in, slide-in, and pulse animations
- **Glow effects**: Interactive hover glows on cards
- **Responsive layout**: 2-column desktop, single column mobile
- **Color-coded data**: Intuitive visual feedback for all metrics

## Technologies

- **React 18**: Modern React with hooks
- **Vite**: Fast build tool and dev server
- **CSS Modules**: Component-scoped styling
- **SVG Icons**: Custom hand-crafted icon set

## Next Steps

To integrate with backend:
1. Replace sample data with API calls
2. Connect WebSocket for real-time analysis
3. Add authentication
4. Implement data persistence
5. Add meal history and trends
