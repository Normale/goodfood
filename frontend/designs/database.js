{activeTab === 'database' && (
<motion.div key="database" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
    className="grid grid-cols-1 lg:grid-cols-2 gap-6">
    {/* Food Explorer */}
    <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-lg p-6">
        <div className="flex items-center gap-3 mb-6">
            <div
                className="w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                <Database className="w-6 h-6 text-white" />
            </div>
            <div>
                <h3 className="text-lg font-semibold text-white">Browse Foods</h3>
                <p className="text-sm text-white/60">Complete nutrient profiles</p>
            </div>
        </div>

        <div className="space-y-3">
            {[
            { name: 'Salmon (Atlantic, wild)', category: 'Fish & Seafood', protein: 25.4, carbs: 0, fats: 13.4,
            highlight: 'EPA+DHA: 2260mg' },
            { name: 'Spinach (raw)', category: 'Vegetables', protein: 2.9, carbs: 3.6, fats: 0.4, highlight: 'Vitamin K:
            483mcg' },
            { name: 'Almonds (raw)', category: 'Nuts & Seeds', protein: 21.2, carbs: 21.6, fats: 49.9, highlight:
            'Vitamin E: 25.6mg' },
            { name: 'Blueberries (fresh)', category: 'Fruits', protein: 0.7, carbs: 14.5, fats: 0.3, highlight:
            'Polyphenols: 560mg' },
            { name: 'Eggs (whole, large)', category: 'Protein Sources', protein: 6.3, carbs: 0.6, fats: 5.3, highlight:
            'Choline: 147mg' },
            ].map((food, index) => (
            <motion.div key={food.name} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{
                delay: index * 0.1 }}
                className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-all cursor-pointer">
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
            <div
                className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center">
                <Database className="w-6 h-6 text-white" />
            </div>
            <div>
                <h3 className="text-lg font-semibold text-white">Add to Database</h3>
                <p className="text-sm text-white/60">Expand your food library</p>
            </div>
        </div>

        <div className="space-y-4">
            <div>
                <label className="block text-sm font-medium text-white/70 mb-2">Food Name</label>
                <input type="text" placeholder="e.g., Grilled Chicken Breast"
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50" />
            </div>

            <div>
                <label className="block text-sm font-medium text-white/70 mb-2">Category</label>
                <select
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50">
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
                    <input type="number" placeholder="0"
                        className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Carbs (g)</label>
                    <input type="number" placeholder="0"
                        className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50" />
                </div>
                <div>
                    <label className="block text-sm font-medium text-white/70 mb-2">Fats (g)</label>
                    <input type="number" placeholder="0"
                        className="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50" />
                </div>
            </div>

            <div>
                <label className="block text-sm font-medium text-white/70 mb-2">Key Nutrients</label>
                <textarea placeholder="e.g., Vitamin B12: 2.5mcg, Iron: 1.2mg" rows={3}
                    className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-2 focus:ring-purple-500/50 resize-none" />
            </div>

            <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}
                className="w-full px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-pink-600 text-white font-medium shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 transition-all">
                Add to Database
            </motion.button>
        </div>
    </div>
</motion.div>
)}