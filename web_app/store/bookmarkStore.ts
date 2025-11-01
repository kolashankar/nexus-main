import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface BookmarkState {
  jobs: string[];
  internships: string[];
  scholarships: string[];
  articles: string[];
  dsa: string[];
  roadmaps: string[];
  bookmarks: {
    jobs: string[];
    internships: string[];
    scholarships: string[];
    articles: string[];
    dsa: string[];
    roadmaps: string[];
  };
  
  toggleJobBookmark: (id: string) => void;
  toggleInternshipBookmark: (id: string) => void;
  toggleScholarshipBookmark: (id: string) => void;
  toggleArticleBookmark: (id: string) => void;
  removeBookmark: (type: string, id: string) => void;
  
  isJobBookmarked: (id: string) => boolean;
  isInternshipBookmarked: (id: string) => boolean;
  isScholarshipBookmarked: (id: string) => boolean;
  isArticleBookmarked: (id: string) => boolean;
}

export const useBookmarkStore = create<BookmarkState>()(
  persist(
    (set, get) => ({
      jobs: [],
      internships: [],
      scholarships: [],
      articles: [],
      dsa: [],
      roadmaps: [],
      bookmarks: {
        jobs: [],
        internships: [],
        scholarships: [],
        articles: [],
        dsa: [],
        roadmaps: [],
      },

      toggleJobBookmark: (id: string) => {
        set((state) => {
          const newJobs = state.jobs.includes(id)
            ? state.jobs.filter((jobId) => jobId !== id)
            : [...state.jobs, id];
          return {
            jobs: newJobs,
            bookmarks: { ...state.bookmarks, jobs: newJobs }
          };
        });
      },

      toggleInternshipBookmark: (id: string) => {
        set((state) => {
          const newInternships = state.internships.includes(id)
            ? state.internships.filter((internshipId) => internshipId !== id)
            : [...state.internships, id];
          return {
            internships: newInternships,
            bookmarks: { ...state.bookmarks, internships: newInternships }
          };
        });
      },

      toggleScholarshipBookmark: (id: string) => {
        set((state) => {
          const newScholarships = state.scholarships.includes(id)
            ? state.scholarships.filter((scholarshipId) => scholarshipId !== id)
            : [...state.scholarships, id];
          return {
            scholarships: newScholarships,
            bookmarks: { ...state.bookmarks, scholarships: newScholarships }
          };
        });
      },

      toggleArticleBookmark: (id: string) => {
        set((state) => {
          const newArticles = state.articles.includes(id)
            ? state.articles.filter((articleId) => articleId !== id)
            : [...state.articles, id];
          return {
            articles: newArticles,
            bookmarks: { ...state.bookmarks, articles: newArticles }
          };
        });
      },

      removeBookmark: (type: string, id: string) => {
        set((state) => {
          const currentList = state[type as keyof typeof state] as string[];
          if (Array.isArray(currentList)) {
            const newList = currentList.filter((itemId) => itemId !== id);
            return {
              [type]: newList,
              bookmarks: { ...state.bookmarks, [type]: newList }
            };
          }
          return state;
        });
      },

      isJobBookmarked: (id: string) => get().jobs.includes(id),
      isInternshipBookmarked: (id: string) => get().internships.includes(id),
      isScholarshipBookmarked: (id: string) => get().scholarships.includes(id),
      isArticleBookmarked: (id: string) => get().articles.includes(id),
    }),
    {
      name: 'bookmark-storage',
    }
  )
);
