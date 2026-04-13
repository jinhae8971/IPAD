import { render, screen } from '@testing-library/react';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
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
  // Layout/Sidebar/Home/Agents/AgentDetail all read from React Query
  // hooks now. Static seed is still served via placeholderData so the
  // assertions below match without any network.
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
}

describe('Layout', () => {
  it('renders the AI Workstation brand', () => {
    renderAt('/');
    expect(screen.getByRole('heading', { level: 1, name: /AI Workstation/i })).toBeInTheDocument();
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
