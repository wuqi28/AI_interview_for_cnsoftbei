import axios from 'axios'

const axiosLocal = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 120000
})

export default axiosLocal
