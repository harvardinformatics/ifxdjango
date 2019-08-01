import axios from 'axios'
import auth from '../auth'
import { API_ROOT } from '@/urls'


export class APIService {
  constructor () {
    this.auth = auth
  }
}