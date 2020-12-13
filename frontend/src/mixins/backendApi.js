'use strict'
import Axios from 'axios'

export default function backendApi () {
  const axios = Axios.create({
    baseURL: process.env.BACKEND_URL,
    headers: process.env.AXIOS_HEADER,
    responseType: process.env.AXIOS_RESPONSE_TYPE
  })
  return axios
}
