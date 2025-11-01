import AsyncStorage from '@react-native-async-storage/async-storage';

const BOOKMARKS_KEY = '@careerguide_bookmarks';

export interface Bookmark {
  id: string;
  type: 'job' | 'internship' | 'scholarship' | 'article' | 'question' | 'sheet' | 'roadmap';
  data: any;
  bookmarkedAt: string;
}

// Get all bookmarks
export const getBookmarks = async (): Promise<Bookmark[]> => {
  try {
    const bookmarksJson = await AsyncStorage.getItem(BOOKMARKS_KEY);
    return bookmarksJson ? JSON.parse(bookmarksJson) : [];
  } catch (error) {
    console.error('Error getting bookmarks:', error);
    return [];
  }
};

// Get bookmarks by type
export const getBookmarksByType = async (type: Bookmark['type']): Promise<Bookmark[]> => {
  const bookmarks = await getBookmarks();
  return bookmarks.filter((b) => b.type === type);
};

// Check if item is bookmarked
export const isBookmarked = async (id: string): Promise<boolean> => {
  const bookmarks = await getBookmarks();
  return bookmarks.some((b) => b.id === id);
};

// Add bookmark
export const addBookmark = async (
  id: string,
  type: Bookmark['type'],
  data: any
): Promise<boolean> => {
  try {
    const bookmarks = await getBookmarks();
    
    // Check if already bookmarked
    if (bookmarks.some((b) => b.id === id)) {
      return false;
    }

    const newBookmark: Bookmark = {
      id,
      type,
      data,
      bookmarkedAt: new Date().toISOString(),
    };

    bookmarks.push(newBookmark);
    await AsyncStorage.setItem(BOOKMARKS_KEY, JSON.stringify(bookmarks));
    return true;
  } catch (error) {
    console.error('Error adding bookmark:', error);
    return false;
  }
};

// Remove bookmark
export const removeBookmark = async (id: string): Promise<boolean> => {
  try {
    const bookmarks = await getBookmarks();
    const filtered = bookmarks.filter((b) => b.id !== id);
    await AsyncStorage.setItem(BOOKMARKS_KEY, JSON.stringify(filtered));
    return true;
  } catch (error) {
    console.error('Error removing bookmark:', error);
    return false;
  }
};

// Toggle bookmark
export const toggleBookmark = async (
  id: string,
  type: Bookmark['type'],
  data: any
): Promise<boolean> => {
  const bookmarked = await isBookmarked(id);
  if (bookmarked) {
    return await removeBookmark(id);
  } else {
    return await addBookmark(id, type, data);
  }
};

// Get all bookmarks (alias for getBookmarks for consistency)
export const getAllBookmarks = async (): Promise<Array<{
  id: string;
  type: Bookmark['type'];
  data: any;
  savedAt: number;
}>> => {
  const bookmarks = await getBookmarks();
  return bookmarks.map(b => ({
    id: b.id,
    type: b.type,
    data: b.data,
    savedAt: new Date(b.bookmarkedAt).getTime(),
  }));
};
