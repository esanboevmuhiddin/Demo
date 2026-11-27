document.addEventListener('DOMContentLoaded', () => {
    const slider = document.getElementById('slider');
    if (!slider) return;

    const track = slider.querySelector('.slides');
    const imgs = track.querySelectorAll('img');
    const prevBtn = slider.querySelector('.slider-prev');
    const nextBtn = slider.querySelector('.slider-next');
    const dotsBox = slider.querySelector('.slider-dots');
    const total = imgs.length;
    let index = 0;
    let timer = null;

    // Создаем точки
    imgs.forEach((_, i) => {
        const dot = document.createElement('span');
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goTo(i));
        dotsBox.appendChild(dot);
    });
    const dots = dotsBox.querySelectorAll('span');

    function render() {
        track.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((d, i) => d.classList.toggle('active', i === index));
    }

    function goTo(i) {
        index = (i + total) % total;
        render();
        restart();
    }

    function next() { goTo(index + 1); }
    function prev() { goTo(index - 1); }

    function start() { timer = setInterval(next, 3000); }
    function stop() { clearInterval(timer); }
    function restart() { stop(); start(); }

    nextBtn.addEventListener('click', next);
    prevBtn.addEventListener('click', prev);
    slider.addEventListener('mouseenter', stop);
    slider.addEventListener('mouseleave', start);

    start();
});