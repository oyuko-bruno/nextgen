document.addEventListener('DOMContentLoaded', function() {
    restoreFormData();
    // Additional form restoration logic if needed
    });
    
    document.getElementById('addChildTraveler').addEventListener('change', function() {
    const childDetailsSection = document.getElementById('childDetails');
    if (this.checked) {
    childDetailsSection.style.display = 'block';
    sessionStorage.setItem('childTravelerChecked', 'true');
    } else {
    childDetailsSection.style.display = 'none';
    sessionStorage.removeItem('childTravelerChecked');
    }
    saveFormData();
    });
    
    document.getElementById('bookTaxi').addEventListener('change', function() {
    const taxiBookingDetails = document.getElementById('taxiBooking');
    if (this.checked) {
    sessionStorage.setItem('bookTaxiChecked', 'true');
    saveFormData();
    redirectToDriversProfile();
    } else {
    taxiBookingDetails.style.display = 'none';
    sessionStorage.removeItem('bookTaxiChecked');
    }
    saveFormData();
    });
    
    function saveFormData() {
    const formData = new FormData(document.getElementById('bookingForm'));
    for (const [key, value] of formData.entries()) {
    sessionStorage.setItem(key, value);
    }
    sessionStorage.setItem('childTravelerChecked', document.getElementById('addChildTraveler').checked);
    sessionStorage.setItem('bookTaxiChecked', document.getElementById('bookTaxi').checked);
    sessionStorage.setItem('selectSeatChecked', document.getElementById('selectSeatCheckbox').checked);

    const selectedSeats = document.querySelectorAll('.seat.selected');
    const selectedSeatNumbers = Array.from(selectedSeats).map(seat => seat.textContent.trim());
    sessionStorage.setItem('selectedSeatNumbers', selectedSeatNumbers.join(','));
    }
    
    function restoreFormData() {
    const isChildTravelerChecked = sessionStorage.getItem('childTravelerChecked') === 'true';
    document.getElementById('addChildTraveler').checked = isChildTravelerChecked;
    document.getElementById('childDetails').style.display = isChildTravelerChecked ? 'block' : 'none';
    

    const form = document.getElementById('bookingForm');
    for (const key of Object.keys(sessionStorage)) {
        const formElement = form.elements[key];
        if (formElement) {
            if (formElement.type === 'checkbox') {
                formElement.checked = sessionStorage.getItem(key) === 'true';
            } else {
                formElement.value = sessionStorage.getItem(key);
            }
        }
    }
    
    document.getElementById('from').value = sessionStorage.getItem('from') || '';
    document.getElementById('to').value = sessionStorage.getItem('to') || '';
    document.getElementById('trainType').dispatchEvent(new Event('change'));
    
    const selectedSeatNumbers = sessionStorage.getItem('selectedSeatNumbers');
    if (selectedSeatNumbers) {
        const selectedSeatNumbersArray = selectedSeatNumbers.split(',');
        selectedSeatNumbersArray.forEach(seatNumber => {
            const seatElement = document.querySelector(`.seat[data-seat-number="${seatNumber.trim()}"]`);
            if (seatElement) {
                seatElement.classList.add('selected');
            }
        });
    }
    
    const isBookTaxiChecked = sessionStorage.getItem('bookTaxiChecked') === 'true';
    document.getElementById('bookTaxi').checked = isBookTaxiChecked;
    document.getElementById('taxiBooking').style.display = isBookTaxiChecked ? 'block' : 'none';
    
    const isSelectSeatChecked = sessionStorage.getItem('selectSeatChecked') === 'true';
    document.getElementById('selectSeatCheckbox').checked = isSelectSeatChecked;
    if (isSelectSeatChecked) {
        document.getElementById('seatSelectionWindow').classList.add('show');
    }
    }
    
    function redirectToDriversProfile() {
    window.location.href = "{% url 'approved_drivers' %}";
    }
    
    // Functions related to train type selection and session expiry management remain unchanged
    
    const trainStations = {
    "Inter-County": [
    { from: "Nairobi", to: ["Mombasa", "Mariakani"], departureTime: "08:00" },
    { from: "Mombasa", to: ["Nairobi", "Mariakani"], departureTime: "08:00" },
    { from: "Mariakani", to: ["Nairobi", "Mombasa"], departureTime: "10:00" }
    ],
    "Afternoon": [
    { from: "Nairobi", to: ["Mombasa", "Voi"], departureTime: "15:00" },
    { from: "Mombasa", to: ["Nairobi", "Voi"], departureTime: "15:00" },
    { from: "Voi", to: ["Nairobi", "Mombasa"], departureTime: "17:00" }
    ],
    "Night": [
    { from: "Nairobi", to: ["Mombasa"], departureTime: "22:00" },
    { from: "Mombasa", to: ["Nairobi"], departureTime: "22:00" }
    ]
    };
    
    // Event listener for trainType selection change
    document.getElementById('trainType').addEventListener('change', function() {
    const selectedTrainType = this.value;
    const fromSelect = document.getElementById('from');
    const toSelect = document.getElementById('to');
    const timeInput = document.getElementById('time');
    const routes = trainStations[selectedTrainType];
    
    fromSelect.innerHTML = '';
    toSelect.innerHTML = '';
    timeInput.value = '';
    
    routes.forEach(route => {
        const optionFrom = document.createElement('option');
        optionFrom.value = route.from;
        optionFrom.textContent = route.from;
        fromSelect.appendChild(optionFrom);
    });
    
    if (routes.length > 0) {
        timeInput.value = routes[0].departureTime;
    }
    
    updateToStationsAndTime();
    });
    
    // Event listener for from station change
    document.getElementById('from').addEventListener('change', updateToStationsAndTime);
    
    // Function to update to stations and time based on selected train type and from station
    function updateToStationsAndTime() {
    const selectedTrainType = document.getElementById('trainType').value;
    const selectedFromStation = document.getElementById('from').value;
    const selectedRoute = trainStations[selectedTrainType].find(route => route.from === selectedFromStation);
    const toSelect = document.getElementById('to');
    const timeInput = document.getElementById('time');
 
    toSelect.innerHTML = '';
    timeInput.value = '';
    
    if (selectedRoute) {
        selectedRoute.to.forEach(station => {
            const optionTo = document.createElement('option');
            optionTo.value = station;
            optionTo.textContent = station;
            toSelect.appendChild(optionTo);
        });
        timeInput.value = selectedRoute.departureTime;
    }
    }
    
    // Function to handle session management for book taxi checkbox
    const bookTaxiCheckbox = document.getElementById('bookTaxi');
    bookTaxiCheckbox.addEventListener('change', function() {
    if (this.checked) {
    // If bookTaxi is checked, save form data and set a timer for session expiry
    saveFormData();
    setSessionExpiryTimer();
    } else {
    // If bookTaxi is unchecked, clear the timer
    clearSessionExpiryTimer();
    }
    });
    
    // Function to set session expiry timer
    function setSessionExpiryTimer() {
    const expiryTime = 60000; // 1 minute
    window.sessionExpiryTimer = setTimeout(handleSessionExpiry, expiryTime);
    }
    
    // Function
    // Function to clear session expiry timer
    function clearSessionExpiryTimer() {
    clearTimeout(window.sessionExpiryTimer);
    }
    
    // Function to handle session expiry
    function handleSessionExpiry() {
    // Show a message indicating session expiry and redirect to login page
    alert('Your session has expired. Please log in again to continue.');
    // Redirect the user to the login page
    window.location.href = "{% url 'login' %}";
    }
    
    // Function to populate form data from sessionStorage when the page loads
    document.addEventListener('DOMContentLoaded', function() {
    restoreFormData();
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
    const checkboxState = sessionStorage.getItem(checkbox.id);
    if (checkboxState === 'true') {
    checkbox.checked = true;
    if (checkbox.id === 'bookTaxi') {
    document.getElementById('taxiBooking').style.display = 'block';
    }
    }
    });
    const selectedDriver = sessionStorage.getItem('selectedDriver');
    if (selectedDriver) {
    const driverDetails = JSON.parse(selectedDriver);
    // Populate driver details
    }
    });
    
    // Function to redirect to the drivers profile page
    function redirectToDriversProfile() {
    window.location.href = "{% url 'approved_drivers' %}";
    }
    
    // Function to toggle display of insurance options based on checkbox state
    function toggleInsuranceOptions(show) {
    const insuranceOptions = document.getElementById('insuranceOptions');
    insuranceOptions.style.display = show ? 'block' : 'none';
    }
    
    // Event listener for insuranceCheckbox change
    document.getElementById('insuranceCheckbox').addEventListener('change', function() {
    toggleInsuranceOptions(this.checked);
    if (this.checked) {
    populateInsuranceOptions();
    }
    });
    
    // Function to populate insurance options
    function populateInsuranceOptions() {
    const insuranceTypeSelect = document.getElementById('insuranceType');
    // Clear existing options
    insuranceTypeSelect.innerHTML = '';
    // Add new insurance options
    const insuranceTypes = ["Basic", "Classic"]; // Example insurance options
    insuranceTypes.forEach(type => {
    const option = document.createElement('option');
    option.value = type;
    option.textContent = type;
    insuranceTypeSelect.appendChild(option);
    });
    }
    
    const availableSeats = [
    { seatNumber: '1A', status: 'available' },
    { seatNumber: '1B', status: 'available' },
    { seatNumber: '1C', status: 'unavailable' },
    { seatNumber: '2A', status: 'available' },
    { seatNumber: '2B', status: 'selected' },
    { seatNumber: '2C', status: 'available' }
    ];
    
    // Generate seat elements
    function generateSeatElement(seat) {
    const seatElement = document.createElement('div');
    seatElement.classList.add('seat');
    seatElement.textContent = seat.seatNumber;
    seatElement.setAttribute('data-status', seat.status);
    if (seat.status === 'unavailable') {
    seatElement.classList.add('unavailable');
    seatElement.disabled = true;
    } else {
    seatElement.addEventListener('click', function() {
    this.classList.toggle('selected');
    });
    }
    return seatElement;
    }
    
    // Populate seat map
    function populateSeatMap(seats) {
    const seatMap = document.querySelector('.seat-map');
    seatMap.innerHTML = '';
    seats.forEach(seat => {
    const seatElement = generateSeatElement(seat);
    seatMap.appendChild(seatElement);
    });
    }
    
    // Populate seat map on page load
    populateSeatMap(availableSeats);
    
    // Handle "Select Seat" checkbox change
    document.getElementById('selectSeatCheckbox').addEventListener('change', function() {
    const seatSelectionWindow = document.getElementById('seatSelectionWindow');
    if (this.checked) {
    seatSelectionWindow.classList.add('show');
    } else {
    seatSelectionWindow.classList.remove('show');
    }
    });
    
    // Confirm seat selection
    document.getElementById('confirmSeatButton').addEventListener('click', function(event) {
    event.preventDefault();
    const selectedSeats = document.querySelectorAll('.seat.selected');
    if (selectedSeats.length === 0) {
    alert('Please select a seat before proceeding.');
    } else {
    const selectedSeatNumbers = Array.from(selectedSeats).map(seat => seat.textContent);
    document.getElementById('selectedSeatInput').value = selectedSeatNumbers.join(', ');
    document.getElementById('seatSelectionWindow').classList.remove('show');
    }
    });
    
    // Handle form submission
    document.getElementById('bookingForm').addEventListener('submit', function(event) {
    const selectSeatChecked = document.getElementById('selectSeatCheckbox').checked;
    const selectedSeats = document.querySelectorAll('.seat.selected');
    
    if (selectSeatChecked && selectedSeats.length === 0) {
        event.preventDefault();
        alert('Please select a seat before proceeding.');
    }
    });
    
    // Function to save form state in sessionStorage
    function saveFormState() {
    const formState = {
    adultName: document.getElementById('adultName').value,
    dob: document.getElementById('dob').value,
    booking_email_or_phone: document.getElementById('booking_email_or_phone').value,
    addChildTraveler: document.getElementById('addChildTraveler').checked,
    childName: document.getElementById('childName').value,
    childAge: document.getElementById('childAge').value,
    drop: document.getElementById('drop').value,
    pick: document.getElementById('pick').value,
    specialNeeds: document.getElementById('specialNeeds').value,
    travelClass: document.getElementById('travelClass').value,
    trainType: document.getElementById('trainType').value,
    from: document.getElementById('from').value,
    to: document.getElementById('to').value,
    date: document.getElementById('date').value,
    time: document.getElementById('time').value,
    selectedSeatInput: document.getElementById('selectedSeatInput').value,
    meal: document.getElementById('mealCheckbox').checked,
    snack: document.getElementById('snackCheckbox').checked,
    wheelchair: document.getElementById('wheelchairCheckbox').checked,
    insurance: document.getElementById('insuranceCheckbox').checked,
    bookTaxi: document.getElementById('bookTaxi').checked
    };
    sessionStorage.setItem('formState', JSON.stringify(formState));
    }
    
    // Function to load form state from sessionStorage
    function loadFormState() {
    const formState = JSON.parse(sessionStorage.getItem('formState'));
    if (formState) {
    document.getElementById('adultName').value = formState.adultName;
    document.getElementById('dob').value = formState.dob;
    document.getElementById('booking_email_or_phone').value = formState.booking_email_or_phone;
    document.getElementById('addChildTraveler').checked = formState.addChildTraveler;
    document.getElementById('childName').value = formState.childName;
    document.getElementById('childAge').value = formState.childAge;
    document.getElementById('drop').value = formState.drop;
    document.getElementById('pick').value = formState.pick;
    document.getElementById('specialNeeds').value = formState.specialNeeds;
    document.getElementById('travelClass').value = formState.travelClass;
    document.getElementById('trainType').value = formState.trainType;
    document.getElementById('from').value = formState.from;
    document.getElementById('to').value = formState.to;
    document.getElementById('date').value = formState.date;
    document.getElementById('time').value = formState.time;
    document.getElementById('selectedSeatInput').value = formState.selectedSeatInput;
    document.getElementById('mealCheckbox').checked = formState.meal;
    document.getElementById('snackCheckbox').checked = formState.snack;
    document.getElementById('wheelchairCheckbox').checked = formState.wheelchair;
    document.getElementById('insuranceCheckbox').checked = formState.insurance;
    document.getElementById('bookTaxi').checked = formState.bookTaxi;
  
        // Show child details if addChildTraveler was checked
        const ischildDetails = document.getElementById('childDetails');
        ischildDetails.style.display = formState.addChildTraveler ? 'block' : 'none';
    }
    }
    
    // Load form state when the page loads
    document.addEventListener('DOMContentLoaded', () => {
    loadFormState();
    });
    
    // Function to save form state before redirecting
    function saveFormStateBeforeRedirect() {
    const currentURL = window.location.href;
    if (currentURL.includes('approved-drivers-page-url')) {
    saveFormData();
    }
    }
    
    // Function to redirect to the drivers profile page
    function redirectToDriversProfile() {
    window.location.href = "{% url 'approved_drivers' %}";
    }
    
    // Function to populate insurance options
    populateInsuranceOptions();
    
    // Function to populate seat map on page load
    populateSeatMap(availableSeats);
