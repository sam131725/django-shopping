import { createContext, useContext } from 'react';

// Shared auth state so any page (Products, Cart, ...) can tell whether
// there's a logged-in user without re-fetching /api/auth/user/ itself.
export const AuthContext = createContext({ user: undefined, refreshUser: async () => {} });

export function useAuth() {
  return useContext(AuthContext);
}
