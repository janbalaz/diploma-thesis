import * as axios from 'axios'

axios.defaults.baseURL = 'http://localhost:5000'
axios.defaults.headers = {'Content-Type': 'application/json'}

export default axios
