import AsyncStorage from '@react-native-async-storage/async-storage';

const SEARCH_HISTORY_PREFIX = '@careerguide_search_';
const MAX_HISTORY_ITEMS = 10;

export interface SearchHistoryItem {
  query: string;
  timestamp: number;
}

// Get search history for a specific module
export const getSearchHistory = async (module: string): Promise<SearchHistoryItem[]> => {
  try {
    const key = `${SEARCH_HISTORY_PREFIX}${module}`;
    const history = await AsyncStorage.getItem(key);
    return history ? JSON.parse(history) : [];
  } catch (error) {
    console.error('Error getting search history:', error);
    return [];
  }
};

// Add search query to history
export const addSearchHistory = async (module: string, query: string): Promise<void> => {
  try {
    if (!query.trim()) return;

    const key = `${SEARCH_HISTORY_PREFIX}${module}`;
    const history = await getSearchHistory(module);

    // Remove duplicate if exists
    const filtered = history.filter(item => item.query.toLowerCase() !== query.toLowerCase());

    // Add new item at the beginning
    const newHistory: SearchHistoryItem[] = [
      { query: query.trim(), timestamp: Date.now() },
      ...filtered,
    ].slice(0, MAX_HISTORY_ITEMS);

    await AsyncStorage.setItem(key, JSON.stringify(newHistory));
  } catch (error) {
    console.error('Error adding search history:', error);
  }
};

// Clear search history for a module
export const clearSearchHistory = async (module: string): Promise<void> => {
  try {
    const key = `${SEARCH_HISTORY_PREFIX}${module}`;
    await AsyncStorage.removeItem(key);
  } catch (error) {
    console.error('Error clearing search history:', error);
  }
};

// Remove specific search item
export const removeSearchHistoryItem = async (module: string, query: string): Promise<void> => {
  try {
    const history = await getSearchHistory(module);
    const filtered = history.filter(item => item.query !== query);
    const key = `${SEARCH_HISTORY_PREFIX}${module}`;
    await AsyncStorage.setItem(key, JSON.stringify(filtered));
  } catch (error) {
    console.error('Error removing search history item:', error);
  }
};

// Clear all search history (all modules)
export const clearAllSearchHistory = async (): Promise<void> => {
  try {
    const keys = await AsyncStorage.getAllKeys();
    const searchKeys = keys.filter(key => key.startsWith(SEARCH_HISTORY_PREFIX));
    await AsyncStorage.multiRemove(searchKeys);
  } catch (error) {
    console.error('Error clearing all search history:', error);
  }
};
