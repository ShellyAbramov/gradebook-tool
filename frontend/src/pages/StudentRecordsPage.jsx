import {useState, useEffect} from 'react';
import Axios from '../services/Axios';

const StudentRecordsPage = () => {

    const [students, setStudents] = useState([]); 
    const fetchStudents = async () => {
      const response = await Axios.get('/student_info');
      setStudents(response.data);
    };

    const formatDate = (dateString) => {
      const [ year, month, day] = dateString.split('-');
      return `${month}/${day}/${year}`;
    };

    useEffect(() => {
      fetchStudents();
    }, []);

  return (

    <div>
      <div className='container'>
        <h1 className='mt-5'>Students Records</h1>
        <table className='table table-striped table-bordered table-hover mt-2'>
          <thead>
            <tr>
              <th scope='col'>Name</th>
              <th scope='col'>Birthdate</th>
              <th scope='col'>Major</th>
              <th scope='col'>Graduation Year</th>
              <th scope='col'>GPA</th>
              <th scope='col'>Student ID #</th>
            </tr>
          </thead>


          <tbody>
            {students.map((student, index) => (
              <tr key={student.student_id_number || index}>
                <td>{student.name}</td>
                <td>{formatDate(student.birthdate)}</td>
                <td>{student.major}</td>
                <td>{student.graduation_year}</td>
                <td>{student.gpa ? student.gpa.toFixed(2) : 'N/A'}</td>
                <td>{student.student_id_number}</td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  )
}

export default StudentRecordsPage