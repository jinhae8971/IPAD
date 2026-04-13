import { Outlet } from 'react-router-dom';
import TopTabs from './TopTabs';
import Sidebar from './Sidebar';
import './Layout.css';

/**
 * Top-level chrome for the AI Workstation web home.
 *
 * Header → TopTabs → (Sidebar + Outlet)
 */
export default function Layout() {
  return (
    <div className="layout">
      <header className="layout__header">
        <div className="layout__brand">
          <span className="layout__logo">◈</span>
          <div>
            <h1 className="layout__title">AI Workstation</h1>
            <p className="layout__tagline">셀프호스팅형 바이브코딩 플랫폼</p>
          </div>
        </div>
        <TopTabs />
      </header>
      <div className="layout__body">
        <Sidebar />
        <main className="layout__content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
