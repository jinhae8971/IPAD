import { render, screen, fireEvent, within } from '@testing-library/react';
import { RouterProvider, createMemoryRouter } from 'react-router-dom';
import Layout from '../components/Layout';
import Agents from './Agents';
import AgentDetail from './AgentDetail';

function renderAt(path: string) {
  const router = createMemoryRouter(
    [
      {
        path: '/',
        element: <Layout />,
        children: [
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

// Scope queries to the main content region so we don't collide with the
// sidebar (which also lists agents by name).
function mainRegion() {
  return within(screen.getByRole('main'));
}

describe('Agents page', () => {
  it('filters agents by category chip', () => {
    renderAt('/agents');
    expect(mainRegion().getByText('Code Architect')).toBeInTheDocument();
    expect(mainRegion().getByText('Market Analyst')).toBeInTheDocument();

    fireEvent.click(mainRegion().getByRole('button', { name: '분석' }));

    expect(mainRegion().getByText('Market Analyst')).toBeInTheDocument();
    expect(mainRegion().queryByText('Code Architect')).not.toBeInTheDocument();
  });

  it('searches by name', () => {
    renderAt('/agents');
    const input = mainRegion().getByRole('searchbox', { name: /에이전트 검색/ });
    fireEvent.change(input, { target: { value: 'indexer' } });
    expect(mainRegion().getByText('Indexer')).toBeInTheDocument();
    expect(mainRegion().queryByText('Code Architect')).not.toBeInTheDocument();
  });

  it('renders agent detail via nested route', () => {
    renderAt('/agents/code-reviewer');
    expect(
      mainRegion().getByRole('heading', { name: /Code Reviewer/i }),
    ).toBeInTheDocument();
    expect(mainRegion().getByText(/diff 기반 리뷰/)).toBeInTheDocument();
  });
});
