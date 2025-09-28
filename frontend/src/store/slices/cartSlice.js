import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import toast from 'react-hot-toast';

// Async thunks
export const fetchCart = createAsyncThunk(
  'cart/fetchCart',
  async (_, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await axios.get('/api/my-cart/', {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
        },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch cart');
    }
  }
);

export const addToCart = createAsyncThunk(
  'cart/addToCart',
  async ({ itemId, quantity = 1 }, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await axios.post(`/api/items/${itemId}/add_to_cart/`, 
        { quantity },
        {
          headers: {
            'Authorization': `Bearer ${auth.token}`,
          },
        }
      );
      toast.success('Item added to cart!');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to add to cart');
    }
  }
);

export const removeFromCart = createAsyncThunk(
  'cart/removeFromCart',
  async (cartItemId, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      await axios.delete(`/api/carts/items/${cartItemId}/`, {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
        },
      });
      toast.success('Item removed from cart!');
      return cartItemId;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to remove from cart');
    }
  }
);

export const updateCartQuantity = createAsyncThunk(
  'cart/updateCartQuantity',
  async ({ cartItemId, quantity }, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await axios.patch(`/api/carts/items/${cartItemId}/`, 
        { quantity },
        {
          headers: {
            'Authorization': `Bearer ${auth.token}`,
          },
        }
      );
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update quantity');
    }
  }
);

export const checkout = createAsyncThunk(
  'cart/checkout',
  async (checkoutData, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await axios.post('/api/carts/checkout/', 
        checkoutData,
        {
          headers: {
            'Authorization': `Bearer ${auth.token}`,
          },
        }
      );
      toast.success('Order placed successfully!');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Checkout failed');
    }
  }
);

const initialState = {
  items: [],
  loading: false,
  error: null,
  totalItems: 0,
  totalPrice: 0,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearCart: (state) => {
      state.items = [];
      state.totalItems = 0;
      state.totalPrice = 0;
    },
    updateTotals: (state) => {
      state.totalItems = state.items.reduce((sum, item) => sum + item.quantity, 0);
      state.totalPrice = state.items.reduce((sum, item) => sum + (item.item.price * item.quantity), 0);
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Cart
      .addCase(fetchCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCart.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.items || [];
        state.totalItems = action.payload.total_items || 0;
        state.totalPrice = action.payload.total_price || 0;
      })
      .addCase(fetchCart.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to fetch cart');
      })
      
      // Add to Cart
      .addCase(addToCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addToCart.fulfilled, (state, action) => {
        state.loading = false;
        // Update cart items if needed
        if (action.payload.items) {
          state.items = action.payload.items;
          state.totalItems = action.payload.total_items;
          state.totalPrice = action.payload.total_price;
        }
      })
      .addCase(addToCart.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to add item to cart');
      })
      
      // Remove from Cart
      .addCase(removeFromCart.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(removeFromCart.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter(item => item.id !== action.payload);
        cartSlice.caseReducers.updateTotals(state);
      })
      .addCase(removeFromCart.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to remove item from cart');
      })
      
      // Update Cart Quantity
      .addCase(updateCartQuantity.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateCartQuantity.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.items.findIndex(item => item.id === action.payload.id);
        if (index !== -1) {
          state.items[index] = action.payload;
        }
        cartSlice.caseReducers.updateTotals(state);
      })
      .addCase(updateCartQuantity.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to update quantity');
      })
      
      // Checkout
      .addCase(checkout.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(checkout.fulfilled, (state) => {
        state.loading = false;
        state.items = [];
        state.totalItems = 0;
        state.totalPrice = 0;
      })
      .addCase(checkout.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Checkout failed');
      });
  },
});

export const { clearError, clearCart, updateTotals } = cartSlice.actions;
export default cartSlice.reducer;
