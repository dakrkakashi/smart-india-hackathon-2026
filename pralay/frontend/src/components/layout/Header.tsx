export default function Header() {
  return (
    <header className="bg-gray-900 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Pralay</h1>
          <p className="text-sm text-gray-400">Flash Flood Prediction System</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm text-gray-300">NDRF Control Room</p>
            <p className="text-xs text-gray-500">{new Date().toLocaleString()}</p>
          </div>
        </div>
      </div>
    </header>
  )
}
