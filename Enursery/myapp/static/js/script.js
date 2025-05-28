document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
      const link = card.querySelector('a');
      if (link) {
        link.click();
      }
    });
  });

  
  document.body.style.backgroundColor = 'black';

  
