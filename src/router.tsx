import { createHashRouter, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import GettingStarted from './pages/GettingStarted';
import Agents from './pages/Agents';
import AgentDetail from './pages/AgentDetail';
import ApiProviders from './pages/ApiProviders';
import Advanced from './pages/Advanced';
import Workloads from './pages/Workloads';
import WorkloadDetail from './pages/WorkloadDetail';

/**
 * Hash-based router so the SPA works on GitHub Pages without
 * server-side rewrite rules.
 */
export const router = createHashRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      { index: true, element: <Home /> },
      { path: 'getting-started', element: <GettingStarted /> },
      {
        path: 'agents',
        element: <Agents />,
        children: [{ path: ':agentId', element: <AgentDetail /> }],
      },
      { path: 'api-providers', element: <ApiProviders /> },
      { path: 'advanced', element: <Advanced /> },
      { path: 'workloads', element: <Workloads /> },
      { path: 'workloads/:workloadId', element: <WorkloadDetail /> },
      { path: '*', element: <Navigate to="/" replace /> },
    ],
  },
]);
