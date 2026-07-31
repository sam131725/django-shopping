import { useEffect, useState, useCallback } from 'react';
import { Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { api } from './api';
import { AuthContext } from './AuthContext.jsx';
import Login from './pages/Login.jsx';
import Products from './pages/Products.jsx';
import Cart from './pages/Cart.jsx';

export default function App() {
  const [user, setUser] = useState(undefined); // undefined = still checking, null = anonymous
  const navigate = useNavigate();

  const refreshUser = useCallback(async () => {
    try {
      const data = await api.currentUser();
      setUser(data.isAuthenticated ? data.user : null);
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    // Grab the CSRF cookie once up front so any page can add/remove cart
    // items immediately, without needing to have just gone through Login.
    api.csrf().finally(refreshUser);
  }, [refreshUser]);

  async function handleLogout() {
    await api.csrf();
    await api.logout();
    setUser(null);
    navigate('/login');
  }

  if (user === undefined) {
    return <div className="page">Loading…</div>;
  }

  return (
    <AuthContext.Provider value={{ user, refreshUser }}>
      <div>
        <nav className="navbar">
          <Link to="/" className="brand">LezzShop</Link>
          <div className="nav-links">
            <Link to="/">Products</Link>
            {user && <Link to="/cart">Cart</Link>}
            {user ? (
              <>
                <span className="nav-user">Hi, {user.username}</span>
                <button onClick={handleLogout}>Log out</button>
              </>
            ) : (
              <Link to="/login">Log in</Link>
            )}
          </div>
        </nav>

        <main className="page">
          <Routes>
            <Route path="/" element={<Products />} />
            <Route
              path="/login"
              element={user ? <Navigate to="/" replace /> : <Login onLoggedIn={refreshUser} />}
            />
            <Route
              path="/cart"
              element={user ? <Cart /> : <Navigate to="/login" replace />}
            />
          </Routes>
        </main>
      </div>
    </AuthContext.Provider>
  );
}
