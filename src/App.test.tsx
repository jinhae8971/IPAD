import { render, screen } from '@testing-library/react';
import App from './App';

describe('App', () => {
  it('renders the AI Workstation header', () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: /AI Workstation/i })).toBeInTheDocument();
  });
});
