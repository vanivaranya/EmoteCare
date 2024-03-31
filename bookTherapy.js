function showTherapistList(category) {
    const therapistLists = document.getElementsByClassName('therapist-list');
    for (let i = 0; i < therapistLists.length; i++) {
        therapistLists[i].style.display = 'none';
    }
    document.getElementById(category + '-therapist-list').style.display = 'block';
}

function showScheduleForm(category, therapistIndex) {
    const scheduleForm = document.querySelectorAll('#' + category + '-therapist-list .schedule-form')[therapistIndex];
    if (scheduleForm.style.display === 'none' || scheduleForm.style.display === '') {
        scheduleForm.style.display = 'block';
    } else {
        scheduleForm.style.display = 'none';
    }
}
