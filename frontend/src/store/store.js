/**
 * Zustand store для управления состоянием приложения
 */

import { create } from 'zustand';

/**
 * Store для коов
 */
export const useCowStore = create((set) => ({
  cows: [],
  currentCow: null,
  loading: false,
  error: null,
  
  // Actions
  setCows: (cows) => set({ cows }),
  setCurrentCow: (cow) => set({ currentCow: cow }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
  
  addCow: (cow) => set((state) => ({
    cows: [...state.cows, cow]
  })),
  
  updateCow: (cowId, updatedCow) => set((state) => ({
    cows: state.cows.map(cow => cow.id === cowId ? updatedCow : cow),
    currentCow: state.currentCow?.id === cowId ? updatedCow : state.currentCow
  })),
  
  removeCow: (cowId) => set((state) => ({
    cows: state.cows.filter(cow => cow.id !== cowId),
    currentCow: state.currentCow?.id === cowId ? null : state.currentCow
  })),
  
  clearError: () => set({ error: null })
}));

/**
 * Store для распознавания
 */
export const useRecognitionStore = create((set) => ({
  recognitionResult: null,
  recognitionLoading: false,
  recognitionError: null,
  
  // Video stream
  isVideoActive: false,
  lastDetection: null,
  
  // Actions
  setRecognitionResult: (result) => set({ recognitionResult: result }),
  setRecognitionLoading: (loading) => set({ recognitionLoading: loading }),
  setRecognitionError: (error) => set({ recognitionError: error }),
  
  setVideoActive: (active) => set({ isVideoActive: active }),
  setLastDetection: (detection) => set({ lastDetection: detection }),
  
  clearRecognitionResult: () => set({ recognitionResult: null }),
  clearRecognitionError: () => set({ recognitionError: null })
}));

/**
 * Store для UI состояния
 */
export const useUIStore = create((set) => ({
  currentPage: 'home', // 'home', 'admin', 'recognition'
  sidebarOpen: true,
  
  setCurrentPage: (page) => set({ currentPage: page }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen }))
}));
