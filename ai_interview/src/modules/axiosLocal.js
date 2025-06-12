import axios from 'axios'

const axiosLocal = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 60000
})

export default axiosLocal
