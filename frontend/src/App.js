import { useEffect, useState } from 'react';
import { Segment, Rail } from 'semantic-ui-react';
import axios from 'axios';

import './App.css';

import Map from './components/map';
import Sidebar from './components/sidebar';

function App() {

    const [stats, setStats] = useState({
        totalCases: '',
        newCasesSmoothed: '',
        totalDeaths: '',
        lastUpdateDate: '',
        reproductionRate: '',
        peopleFullyVaccinatedPerHundred: ''
    })
    const [location, setLocation] = useState('Australia');

    useEffect(() => {
        if (location !== '') {
            fetchStats(location)
        }
    }, [location]);

    // request for stats from backend
    const fetchStats = async location => {

        const config = {
            method: 'post',
            url: 'http://localhost:4000/stats',
            responseType: 'json',
            data: { location: location }
        }

        try {
            const resp = await axios(config)
            setStats({
                totalDeaths: resp.data['total_deaths'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','),
                totalCases: resp.data['total_cases'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','),
                newCasesSmoothed: resp.data['new_cases_smoothed'].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ','),
                lastUpdateDate: resp.data['last_update_date'],
                reproductionRate: resp.data['reproduction_rate'],
                peopleFullyVaccinatedPerHundred: resp.data['people_fully_vaccinated_per_hundred']
            })
            console.log('fetched')
        } catch (e) {
            console.log(e);
        }
    }

    return (
        <div className="App">

            <Map location={location} onChange={location => setLocation(location)} />

            <Rail attached internal position='left'>
                <Segment>
                    <Sidebar
                        location={location}
                        totalDeaths={stats.totalDeaths}
                        totalCases={stats.totalCases}
                        newCasesSmoothed={stats.newCasesSmoothed}
                        lastUpdateDate={stats.lastUpdateDate}
                        reproductionRate={stats.reproductionRate}
                        peopleFullyVaccinatedPerHundred={stats.peopleFullyVaccinatedPerHundred}
                        onChange={locations => setLocation(locations)}
                        fetchStats={fetchStats}
                    />
                </Segment>
            </Rail>

            <p>Data from <a href='https://ourworldindata.org/coronavirus'>Our World in Data</a></p>
        </div>
    );
}

export default App;