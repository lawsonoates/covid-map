import { useEffect, useState } from 'react';
import { Segment, Rail } from 'semantic-ui-react';
import axios from 'axios';

import './App.css';

import Map from './components/map';
import Sidebar from './components/sidebar';

function App() {

    const [stats, setStats] = useState({
        deaths: '',
        confirmed: '',
        status: ''
    })
    const [location, setLocation] = useState('Australia');
    // const [iso, setISO] = useState('');

    useEffect(() => {
        if (location !== '') {
            fetchStats(location)
        }
    }, [location]);

    const fetchStats = async location => {

        const config = {
            method: 'post',
            url: 'http://localhost:4000/stats',
            responseType: 'json',
            data: { location: location }
        }

        try {
            // console.log(config.data)
            const resp = await axios(config)
            setStats({
                deaths: resp.data['deaths'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','),
                confirmed: resp.data['confirmed'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
            })
        } catch (e) {
            console.log(e);
        }
    }

    return (
        <div className="App">
            <Segment>
                <Map location={location} onChange={location => setLocation(location)} />

                <Rail attached internal position='left'>
                    <Segment>
                        <Sidebar
                            location={location}
                            deaths={stats.deaths}
                            confirmed={stats.confirmed}
                            status={stats.status}
                            onChange={locations => setLocation(locations)}
                        />
                    </Segment>
                </Rail>
            </Segment>
        </div>
    );
}

export default App;
