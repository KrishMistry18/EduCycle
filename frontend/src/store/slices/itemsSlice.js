import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import toast from 'react-hot-toast';

// Async thunks
export const fetchItems = createAsyncThunk(
  'items/fetchItems',
  async (params = {}, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/items/', { params });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch items');
    }
  }
);

export const fetchItemById = createAsyncThunk(
  'items/fetchItemById',
  async (id, { rejectWithValue }) => {
    try {
      const response = await axios.get(`/api/items/${id}/`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to fetch item');
    }
  }
);

export const searchItems = createAsyncThunk(
  'items/searchItems',
  async (searchParams, { rejectWithValue }) => {
    try {
      const response = await axios.get('/api/search/', { params: searchParams });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Search failed');
    }
  }
);

export const createItem = createAsyncThunk(
  'items/createItem',
  async (itemData, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const formData = new FormData();
      
      // Append all item data to FormData
      Object.keys(itemData).forEach(key => {
        if (key === 'images') {
          itemData[key].forEach((image, index) => {
            formData.append(`image${index + 1}`, image);
          });
        } else {
          formData.append(key, itemData[key]);
        }
      });

      const response = await axios.post('/api/items/', formData, {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
          'Content-Type': 'multipart/form-data',
        },
      });
      
      toast.success('Item created successfully!');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to create item');
    }
  }
);

export const updateItem = createAsyncThunk(
  'items/updateItem',
  async ({ id, itemData }, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      const response = await axios.patch(`/api/items/${id}/`, itemData, {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
        },
      });
      
      toast.success('Item updated successfully!');
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to update item');
    }
  }
);

export const deleteItem = createAsyncThunk(
  'items/deleteItem',
  async (id, { rejectWithValue, getState }) => {
    try {
      const { auth } = getState();
      await axios.delete(`/api/items/${id}/`, {
        headers: {
          'Authorization': `Bearer ${auth.token}`,
        },
      });
      
      toast.success('Item deleted successfully!');
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || 'Failed to delete item');
    }
  }
);

const initialState = {
  items: [],
  currentItem: null,
  searchResults: [],
  filters: {
    category: '',
    minPrice: '',
    maxPrice: '',
    sortBy: '-created_at',
  },
  loading: false,
  searchLoading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
  },
};

const itemsSlice = createSlice({
  name: 'items',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = {
        category: '',
        minPrice: '',
        maxPrice: '',
        sortBy: '-created_at',
      };
    },
    clearSearchResults: (state) => {
      state.searchResults = [];
    },
    setCurrentItem: (state, action) => {
      state.currentItem = action.payload;
    },
    clearCurrentItem: (state) => {
      state.currentItem = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Items
      .addCase(fetchItems.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchItems.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload.results || action.payload;
        state.pagination = {
          count: action.payload.count || 0,
          next: action.payload.next || null,
          previous: action.payload.previous || null,
        };
      })
      .addCase(fetchItems.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to fetch items');
      })
      
      // Fetch Item by ID
      .addCase(fetchItemById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchItemById.fulfilled, (state, action) => {
        state.loading = false;
        state.currentItem = action.payload;
      })
      .addCase(fetchItemById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to fetch item details');
      })
      
      // Search Items
      .addCase(searchItems.pending, (state) => {
        state.searchLoading = true;
        state.error = null;
      })
      .addCase(searchItems.fulfilled, (state, action) => {
        state.searchLoading = false;
        state.searchResults = action.payload.results || action.payload;
      })
      .addCase(searchItems.rejected, (state, action) => {
        state.searchLoading = false;
        state.error = action.payload;
        toast.error('Search failed');
      })
      
      // Create Item
      .addCase(createItem.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createItem.fulfilled, (state, action) => {
        state.loading = false;
        state.items.unshift(action.payload);
      })
      .addCase(createItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to create item');
      })
      
      // Update Item
      .addCase(updateItem.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateItem.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.items.findIndex(item => item.id === action.payload.id);
        if (index !== -1) {
          state.items[index] = action.payload;
        }
        if (state.currentItem?.id === action.payload.id) {
          state.currentItem = action.payload;
        }
      })
      .addCase(updateItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to update item');
      })
      
      // Delete Item
      .addCase(deleteItem.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteItem.fulfilled, (state, action) => {
        state.loading = false;
        state.items = state.items.filter(item => item.id !== action.payload);
        if (state.currentItem?.id === action.payload) {
          state.currentItem = null;
        }
      })
      .addCase(deleteItem.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        toast.error('Failed to delete item');
      });
  },
});

export const {
  clearError,
  setFilters,
  clearFilters,
  clearSearchResults,
  setCurrentItem,
  clearCurrentItem,
} = itemsSlice.actions;

export default itemsSlice.reducer;
