import {Link} from 'react-router-dom';


const NotFoundPage = () => {
  return (
    <div className='container d-flex flex-column align-items-center justify-content-center vh-100'>
        <h1 className='display-1 .text-dark fw-bold'>404</h1>
        <h2 className='display-4 fw-bold'>Page Not Found</h2>
        <p className='lead'>The page you are looking for does not exist.</p>
        <Link to="/" className='btn btn-primary'>Go to Home</Link>
        
    </div>
  )
}

export default NotFoundPage