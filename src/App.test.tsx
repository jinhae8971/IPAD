import { render, screen } from '@testing-library/react';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Agents from './pages/Agents';
import AgentDetail from './pages/AgentDetail';
import { TOP_TABS } from './components/topTabs.constants';

function renderAt(path: string) {
  const router = createMemoryRouter(
    [
      {
        path: '/',
        element: <Layout />,
        children: [
          { index: true, element: <Home /> },
          {
            path: 'agents',
            element: <Agents />,
            children: [{ path: ':agentId', element: <AgentDetail /> }],
          },
        ],
      },
    ],
    { initialEntries: [path] },
  );
  return render(<RouterProvider router={router} />);
}

describe('Layout', () => {
  it('renders the AI Workstation brand', () => {
    renderAt('/');
    expect(screen.getByRole('heading', { name: /AI Workstation/i })).toBeInTheDocument();
  });

  it('renders all six top tabs', () => {
    renderAt('/');
    for (const tab of TOP_TABS) {
      expect(screen.getByRole('link', { name: tab.label })).toBeInTheDocument();
    }
    expect(TOP_TABS).toHaveLength(6);
  });

  it('renders sidebar categories', () => {
    renderAt('/');
    expect(screen.getByRole('button', { name: /코딩/ })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /운영/ })).toBeInTheDocument();
  });

  it('renders an agent detail when navigated to /agents/:id', () => {
    renderAt('/agents/code-architect');
    expect(screen.getByRole('heading', { name: /Code Architect/i })).toBeInTheDocument();
  });
});
