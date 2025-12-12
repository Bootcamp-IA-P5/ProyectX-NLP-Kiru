import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

const api = {
  analyzeVideo: async (url, maxComments = 50) => {
    const response = await axios.post(`${API_BASE_URL}/analyze/video`, {
      url,
      max_comments: maxComments
    })
    return response.data
  },

  predictText: async (text) => {
    const response = await axios.post(`${API_BASE_URL}/predict/transformer`, {
      text
    })
    return response.data
  },

  getMetrics: async () => {
    const response = await axios.get(`${API_BASE_URL}/metrics`)
    return response.data
  },


  compareModels: async (text) => {
    const response = await axios.post(`${API_BASE_URL}/predict/compare`, {
      text
    })
    return response.data
  },

  getHealth: async () => {
    const response = await axios.get(`${API_BASE_URL}/health`)
    return response.data
  }
}

export default api