function searchCar() {
    const carNumber = document.getElementById('carNumber').value.trim();
    if (!carNumber) {
        alert('Iltimos, mashina raqamini kiriting!');
        return;
    }
    const carNumberPattern = /^\d{2} [A-Z] \d{3} [A-Z]{2}$/i;
    if (!carNumberPattern.test(carNumber)) {
        alert('Iltimos, raqamni to‘g‘ri formatda kiriting! Masalan: 30 A 123 AA');
        return;
    }
    document.getElementById('carOwnerInfo').style.display = 'block';
    setTimeout(() => {
        document.getElementById('ownerName').textContent = 'Azizbek Samijonov';
        document.getElementById('carModel').textContent = 'Mashina: Chevrolet Malibu';
        document.getElementById('carYear').textContent = 'Yili: 2022';
        document.getElementById('userAvatar').textContent = 'AS';
    }, 1000);
}
