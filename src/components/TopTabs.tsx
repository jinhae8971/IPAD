import { NavLink } from 'react-router-dom';
import { TOP_TABS } from './topTabs.constants';
import './TopTabs.css';

export default function TopTabs() {
  return (
    <nav className="top-tabs" aria-label="primary">
      {TOP_TABS.map((tab) => (
        <NavLink
          key={tab.to}
          to={tab.to}
          end={tab.end}
          className={({ isActive }) =>
            isActive ? 'top-tabs__link top-tabs__link--active' : 'top-tabs__link'
          }
        >
          {tab.label}
        </NavLink>
      ))}
    </nav>
  );
}
