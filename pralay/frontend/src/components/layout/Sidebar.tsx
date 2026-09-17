import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Map,
  Radio,
  AlertTriangle,
  MapPin
} from 'lucide-react'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/map', icon: Map, label: 'Risk Map' },
  { path: '/sensors', icon: Radio, label: 'Sensors' },
  { path: '/alerts', icon: AlertTriangle, label: 'Alerts' },
  { path: '/regions', icon: MapPin, label: 'Regions' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 border-r border-gray-700">
      <div className="p-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <AlertTriangle className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="font-bold text-white">PRALAY</h2>
            <p className="text-xs text-gray-400">SIH 2026</p>
          </div>
        </div>
      </div>

      <nav className="px-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
