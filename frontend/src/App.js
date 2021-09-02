import { useState } from 'react';
import { Segment, Rail } from 'semantic-ui-react';

import './App.css';

import Map from './components/map';
import Sidebar from './components/sidebar';

function App() {

    // const [region, setRegion] = useState('au');
    const [stats, setStats] = useState({
        region: 'World',
        deaths: 0,
        confirmed: 0
    })

    // useEffect(() => {

    // // });
    // function handleRegionChange() {
    //     region => setRegion(region)

    // }

    return (
        <div className="App">
            <Segment>
                <Map region={stats.region} onChange={stats => setStats(stats)}/>

                <Rail attached internal position='left'>
                    <Segment>
                        <Sidebar region={stats.region} deaths={stats.deaths} confirmed={stats.confirmed}/>
                    </Segment>
                </Rail>
            </Segment>
        </div>
    );
}

export default App;
