# API-rate-limiting-and-DoS-vulnerabilities-in-web-services.
Exploring how web services handle API rate limiting, what happens when limits are exceeded, and testing DoS vulnerabilities. Includes testing with public APIs (like GitHub) and local Flask applications, along with strategies to mitigate such attacks.

## Table of Contents

- [Introduction](#introduction)
- [GitHub API Rate Limit Testing](#github-api-rate-limit-testing)
- [Local API Testing (Flask)](#local-api-testing-flask)
- [Slow Loris Attack Simulation](#slow-loris-attack-simulation)
- [Types of Rate Limiting Techniques](#types-of-rate-limiting-techniques)
- [Conclusion](#conclusion)

## Introduction

API Rate Limiting is a critical defense mechanism used by web services to protect against abuse and Denial-of-Service (DoS) attacks by restricting the number of requests a client can make in a given timeframe.

This project demonstrates:
- How APIs like GitHub's implement rate limits.
- How overloading a local server can simulate DoS vulnerabilities.
- How different rate-limiting strategies affect protection.
- Why some attacks, like Slow Loris, require additional mitigation beyond simple request counting.

## GitHub API Rate Limit Testing

### Base Information
- **API base URL:** `https://api.github.com`
- **Test endpoint:** `/users/octocat`
- **Rate limit check endpoint:** `/rate_limit`

### Limits
- **Unauthenticated:** 60 requests per hour.
- **Authenticated (using Personal Access Token):** 5000 requests per hour.

### Steps

1. **Check Rate Limit (Unauthenticated)**
    ```bash
    curl -i https://api.github.com/users/octocat
    ```
    **Observation:**  
    - Remaining Requests: 52 (out of 60).

2. **View Rate Limit Status**
    ```bash
    curl -i https://api.github.com/rate_limit
    ```

3. **Authenticated Request (Using Personal Access Token)**
    ```bash
    curl -i -H "Authorization: token YOUR_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
    ```

4. **Flooding Test (Light)**
    ```bash
    for i in {1..70}
    do
      curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com/users/octocat
    done
    ```

    **Observation:**  
    - After exceeding the limit, received `403 Forbidden` responses.

5. **Burp Suite Intruder Testing**
    - Sending multiple requests and monitoring for `403` or `429` responses.

## Local API Testing (Flask)

A lightweight Flask server was used to simulate and understand rate limiting.

### Without Rate Limiting
- **Tool Used:** Apache Bench (ab)
    ```bash
    ab -n 1000 -c 1000 http://127.0.0.1:5000/test
    ```
    **Observation:**  
    - Server crashed/reset after handling too many concurrent requests due to Flask’s default single-threaded nature.

### With Basic Rate Limiting
- **Implemented:** Fixed Window Rate Limiting.
- **Test:**
    ```bash
    for i in {1..10}
    do
      curl http://127.0.0.1:5000/test
    done
    ```
    **Observation:**  
    - Server properly rejected the 11th request in a 10-second window.

## Slow Loris Attack Simulation

- **Attack Command:**
    ```bash
    slowloris 127.0.0.1 -p 5000 -s 200
    ```

    **Observation:**
    - Slow Loris attack kept live connections open, causing legitimate users to be unable to connect.
    - Normal API rate limiting methods **do not** protect against Slow Loris attacks.

## Types of Rate Limiting Techniques

| Technique               | Description                                                             |
|--------------------------|-------------------------------------------------------------------------|
| Fixed Window Counter     | Counts requests in fixed time intervals.                               |
| Sliding Window Log       | Records a timestamp log of each request for accurate counting.         |
| Sliding Window Counter   | Smoothes counts over a moving window.                                  |
| Token Bucket             | Adds tokens at a fixed rate; allows bursts if enough tokens are available. |
| Leaky Bucket             | Processes requests at a constant rate, queues excess ones.             |

## Conclusion

- API rate limiting protects services from being abused by excessive requests.
- GitHub enforces strict per-hour limits based on authentication.
- Local servers without concurrency control and rate limiting are vulnerable to DoS.
- **Fixed Window Rate Limiting** works against simple request floods but **not** against connection-holding attacks like **Slow Loris**.
- **Advanced defenses** like Token Bucket and connection timeout management are recommended for better protection.
