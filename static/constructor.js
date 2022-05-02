document.addEventListener('DOMContentLoaded', () => {
  const $form = document.querySelector('#inputData');
  const $inputs = $form.querySelectorAll('input[type="radio"]');
  const $levels = document.querySelectorAll('[name="lvls"]');
  const $shapes = document.querySelectorAll('[name="shape"]');
  const $toppings = document.querySelectorAll('[name="topping"]');
  const $berries = document.querySelectorAll('[name="berries"]');
  const $decors = document.querySelectorAll('[name="decor"]');
  const $summary = $form.querySelector('#result');
  const $letteringInput = $form.querySelector('#words');
  const $dateInput = document.querySelector('#date');
  const dateMaskOptions = {
    mask: '00.00.0000',
  };
  const dateMask = IMask($dateInput, dateMaskOptions);

  const $timeInput = document.querySelector('#time');
  const timeMaskOptions = {
    mask: '00:00',
  };
  const timeMask = IMask($timeInput, timeMaskOptions);
  const $fastDate = document.querySelector('#fast_date');
  const fastDate = new Date($fastDate.value);

  const CAKE_DATA = {
    lvls: {
      name: $levels[0].value,
      price: $levels[0].dataset.price,
    },
    shape: {
      name: $shapes[0].value,
      price: $shapes[0].dataset.price,
    },
    topping: {
      name: $toppings[0].value,
      price: $toppings[0].dataset.price,
    },
    berries: {
      name: $berries[0].value,
      price: $berries[0].dataset.price,
    },
    decors: {
      name: $decors[0].value,
      price: $decors[0].dataset.price,
    },
    words: '',
    date: {
      date: '',
      time: '',
    },
  };

  const calcPrice = () => {
    let summary = 0;
    Object.keys(CAKE_DATA).forEach((option) => {
      const optionValue = CAKE_DATA[option];

      if (optionValue && option !== 'words' && option !== 'date') {
        summary += +optionValue.price;
      }

      if (option === 'words' && optionValue.length > 0) {
        summary += 500;
      }

      if (option === 'date') {
        const date = new Date(`${optionValue.date} ${optionValue.time}`);
        if (date.getTime() < fastDate.getTime()) {
          summary += summary * 0.2;
        }
      }
    });

    return summary;
  };

  $inputs.forEach(($input) => {
    $input.addEventListener('change', () => {
      const name = $input.name;
      const value = $input.value;
      const price = +$input.dataset.price;

      CAKE_DATA[name] = {
        name: value,
        price,
      };

      $summary.innerHTML = calcPrice();
    });
  });

  $letteringInput.addEventListener('change', (e) => {
    CAKE_DATA['words'] = e.target.value.trim();
    $summary.innerHTML = calcPrice();
  });

  $dateInput.addEventListener('change', (e) => {
    CAKE_DATA['date'].date = moment(e.target.value, 'DD.MM.YYYY').format('YYYY-MM-DD');
    $summary.innerHTML = calcPrice();
  });

  $timeInput.addEventListener('change', (e) => {
    CAKE_DATA['date'].time = e.target.value;
    $summary.innerHTML = calcPrice();
  });
});
