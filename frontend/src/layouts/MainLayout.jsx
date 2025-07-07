import {Outlet} from 'react-router-dom';
import NavigationBar from '../components/NavigationBar';

const MainLayout = () => {
    return (
    <>
    <NavigationBar/>
    <Outlet />
    </>
    );
}

export default MainLayout