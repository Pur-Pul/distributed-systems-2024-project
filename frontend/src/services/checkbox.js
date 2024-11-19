import axios from 'axios'
const baseUrl = 'http://localhost:5000/'

const check = async index => {
    const response = await axios.post(`${baseUrl}update/${index}`)
    return response.data
}

const state = async () => {
    const response = await axios.get(baseUrl)
    return response.data
}

export default { check, state }