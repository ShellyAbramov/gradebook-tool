import {useState, useEffect} from 'react';
import Axios from '../services/Axios';

const AddStudentPage = () => {

    const [students, setStudents] = useState([]);
    const[formData, setFormData] = useState({
      name: '',
      birthdate: '',
      major: '',
      graduation_year: '',
      student_id_number: ''
    });

  
    const fetchStudents = async () => {
      const response = await Axios.get('/student_info');
      setStudents(response.data);
    };

    useEffect(() => {
      fetchStudents();
    }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value
    }));
  };

  // Saves to PostgreSQL via API
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      const studentData = {
        name: formData.name,
        birthdate: formData.birthdate,
        major: formData.major,
        graduation_year: parseInt(formData.graduation_year),
        student_id_number: formData.student_id_number
      };

      const response = await Axios.post('/add_student_info', studentData);
      console.log('Student added:', response.data);

      fetchStudents(); // Refresh the list of students after adding a new one

      setFormData({
        name: '',
        birthdate: '',
        major: '',
        graduation_year: '',
        student_id_number: ''
      });

    }catch (error) {
      console.error('Error adding student:', error);
    }
  };

    const formatDate = (dateString) => {
      const [ year, month, day] = dateString.split('-');
      return `${month}/${day}/${year}`;
    };

  
  return (

    <div>
      <div className='container'>
        <form onSubmit = {handleFormSubmit}>
          <div className ='mb-3 mt-3'>
            <label htmlFor='name' className='form-label'>Full Name:</label>
            <input type='text' className='form-control' id='name' name='name' onChange={handleInputChange} value={formData.name} required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='birthdate' className='form-label'>Birthdate:</label>
            <input type='date' className='form-control' id='birthdate' name='birthdate' onChange={handleInputChange} value={formData.birthdate}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='major' className='form-label'>Major:</label>
            <input type='text' className='form-control' id='major' name='major' onChange={handleInputChange} value={formData.major}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='graduation_year' className='form-label'>Graduation Year:</label>
            <input type='number' className='form-control' id='graduation_year' name='graduation_year' onChange={handleInputChange} value={formData.graduation_year}  required/>
          </div>
          <div className ='mb-3 mt-3'>
            <label htmlFor='student_id_number' className='form-label'>Student ID #:</label>
            <input type='text' className='form-control' id='student_id_number' name='student_id_number' onChange={handleInputChange} value={formData.student_id_number}  required/>
          </div>

          <button type='submit' className='btn btn-primary'>Submit</button>

        </form>

        <table className='table table-striped table-bordered table-hover mt-5'>
          <thead>
            <tr>
              <th scope='col'>Name</th>
              <th scope='col'>Birthdate</th>
              <th scope='col'>Major</th>
              <th scope='col'>Graduation Year</th>
              <th scope='col'>Student ID #</th>
            </tr>
          </thead>


          <tbody>
            {students.map((student) => (
              <tr key={student.student_id_number || index}>
                <td>{student.name}</td>
                <td>{formatDate(student.birthdate)}</td>
                <td>{student.major}</td>
                <td>{student.graduation_year}</td>
                <td>{student.student_id_number}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  )
}

export default AddStudentPage