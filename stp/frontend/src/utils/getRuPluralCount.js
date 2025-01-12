export function getRuPluralCount(count, forms) {
  let formIndex;

  if (count % 10 === 1 && count % 100 !== 11) {
    formIndex = 0;
  } else if ([2, 3, 4].includes(count % 10) && ![12, 13, 14].includes(count % 100)) {
    formIndex = 1;
  } else {
    formIndex = 2;
  }

  return `${forms[formIndex]}`;
}