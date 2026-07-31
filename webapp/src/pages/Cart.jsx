import { useEffect, useState } from 'react';
import { api } from '../api';

export default function Cart() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [busyIds, setBusyIds] = useState({}); // { [cartItemId]: true } while a mutation is in flight

  useEffect(() => {
    api
      .cart()
      .then(setItems)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  function setBusy(id, busy) {
    setBusyIds((s) => ({ ...s, [id]: busy }));
  }

  async function handleIncrement(id) {
    setBusy(id, true);
    setError('');
    try {
      const updated = await api.incrementCartItem(id);
      setItems((prev) => prev.map((i) => (i.id === id ? { ...i, quantity: updated.quantity } : i)));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(id, false);
    }
  }

  async function handleDecrement(id) {
    setBusy(id, true);
    setError('');
    try {
      const result = await api.decrementCartItem(id);
      if (result && result.deleted) {
        setItems((prev) => prev.filter((i) => i.id !== id));
      } else {
        setItems((prev) => prev.map((i) => (i.id === id ? { ...i, quantity: result.quantity } : i)));
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(id, false);
    }
  }

  async function handleRemove(id) {
    setBusy(id, true);
    setError('');
    try {
      await api.removeCartItem(id);
      setItems((prev) => prev.filter((i) => i.id !== id));
    } catch (err) {
      setError(err.message);
      setBusy(id, false);
    }
  }

  if (loading) return <p>Loading cart…</p>;

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return (
    <div>
      <h2>Your Cart</h2>
      {error && <p className="error">{error}</p>}
      {items.length === 0 && <p>Your cart is empty.</p>}
      {items.map((item) => (
        <div className="cart-row" key={item.id}>
          {item.image && <img src={item.image} alt={item.title} className="cart-image" />}
          <div className="cart-row-info">
            <strong>{item.title}</strong>
            <p className="muted">₹{item.price} each</p>
          </div>
          <div className="qty-controls">
            <button type="button" disabled={busyIds[item.id]} onClick={() => handleDecrement(item.id)}>
              −
            </button>
            <span className="qty-value">{item.quantity}</span>
            <button type="button" disabled={busyIds[item.id]} onClick={() => handleIncrement(item.id)}>
              +
            </button>
          </div>
          <p className="line-total">₹{(item.price * item.quantity).toFixed(2)}</p>
          <button
            type="button"
            className="remove-btn"
            disabled={busyIds[item.id]}
            onClick={() => handleRemove(item.id)}
          >
            Remove
          </button>
        </div>
      ))}
      {items.length > 0 && <p className="total">Total: ₹{total.toFixed(2)}</p>}
    </div>
  );
}
