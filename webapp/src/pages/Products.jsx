import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api';
import { useAuth } from '../AuthContext.jsx';

export default function Products() {
  const { user } = useAuth();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  // Per-product transient status, e.g. { 3: 'adding' } or { 3: 'added' }
  const [cartStatus, setCartStatus] = useState({});

  useEffect(() => {
    api
      .products()
      .then(setProducts)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  async function handleAddToCart(productId) {
    setCartStatus((s) => ({ ...s, [productId]: 'adding' }));
    try {
      await api.addToCart(productId);
      setCartStatus((s) => ({ ...s, [productId]: 'added' }));
      setTimeout(() => {
        setCartStatus((s) => ({ ...s, [productId]: undefined }));
      }, 1500);
    } catch (err) {
      setCartStatus((s) => ({ ...s, [productId]: undefined }));
      setError(err.message);
    }
  }

  if (loading) return <p>Loading products…</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Products</h2>
      <div className="grid">
        {products.map((p) => (
          <div className="card" key={p.id}>
            {p.image && <img src={p.image} alt={p.title} className="product-image" />}
            <h3>{p.title}</h3>
            <p className="muted">{p.category}</p>
            <p className="price">₹{p.price}</p>
            {user ? (
              <button
                type="button"
                className="add-to-cart-btn"
                disabled={cartStatus[p.id] === 'adding'}
                onClick={() => handleAddToCart(p.id)}
              >
                {cartStatus[p.id] === 'adding'
                  ? 'Adding…'
                  : cartStatus[p.id] === 'added'
                  ? 'Added ✓'
                  : 'Add to Cart'}
              </button>
            ) : (
              <Link to="/login" className="muted">
                Log in to add to cart
              </Link>
            )}
          </div>
        ))}
        {products.length === 0 && <p>No products found.</p>}
      </div>
    </div>
  );
}
