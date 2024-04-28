// place files you want to import through the `$lib` alias in this folder.
function fibo(previous, prePrevious, diff) {
  let arr = [prePrevious, previous];
  let newNbr = prePrevious + previous;
  for (let i = diff; i > 0; i--) {
    arr.push(newNbr);
    prePrevious = previous;
    previous = newNbr;
    newNbr = prePrevious + previous;
  }
  return [arr, previous];
}
function fiboClosure(fibo) {
  let cache = [0, 1];
  return function (n) {
    let diff = n - (cache.length - 1);
    if (diff > 0) {
      const [cacheResult, result] = fibo(cache.pop(), cache.pop(), diff);
      cache = cache.concat(cacheResult);
      return result;
    } else {
      return cache[n];
    }
  };
}
const fiboMemo = fiboClosure(fibo);
export default fiboMemo;
