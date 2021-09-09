import { useState } from 'react';
import { Segment, Rail } from 'semantic-ui-react';

import './App.css';

import Map from './components/map';
import Sidebar from './components/sidebar';

function App() {

    const [stats, setStats] = useState({
        region: 'World',
        deaths: 0,
        confirmed: 0
    })
    const [location, setLocation] = useState('world');

    return (
        <div className="App">
            <Segment>
                <Map region={location} onChange={location => setLocation(location)}/>

                <Rail attached internal position='left'>
                    <Segment>
                        <Sidebar region={location} deaths={stats.deaths} confirmed={stats.confirmed} onChange={location => setLocation(location)}/>
                    </Segment>
                </Rail>
            </Segment>
        </div>
    );
}

export default App;
