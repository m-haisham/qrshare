/* here lay those thee no home */

/**
 * delay function for the given time.
 *
 * example: wait for a second,
 *   `await delay(1000)`
 *
 * @param {number} ms time to wait in milliseconds
 */
const delay = (ms) => new Promise((res) => setTimeout(res, ms));

export { delay };
