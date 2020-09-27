import React, { Component, useLayoutEffect } from "react";
import axios from 'axios';

const api = axios.create({
  baseURL: '/app/api/customers/'
})

export default class Home extends Component {
  state = {
    customers: []
  }

  constructor() {
    super();
    api.get('/').then(res => {
      console.log(res.data)
      this.setState({ customers: res.data })
    })
  }

  render() {
    return (
      <ul>
        {this.state.customers.map(customer =>
          <li key={customer.id}>{customer.name}</li>
        )}
      </ul>
    );
  }
}