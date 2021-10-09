import { useState } from 'react';
import { Search, Label } from 'semantic-ui-react';

import axios from 'axios';

const resultRenderer = ({ location }) => <Label content={location} />

function Searchbar(props) {

    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);

    // requests results of query from backend
    const requestQuery = async query => {
        setLoading(true);

        const config = {
            method: 'post',
            url: 'http://localhost:4000/search/query',
            responseType: 'json',
            data: { query: query }
        }
        if (query.length !== 0) {
            try {
                const resp = await axios(config)
                setResults(resp.data)
            } catch (e) {
                console.log(e);
            }
        } else {
            setResults([])
        }

        setLoading(false);
    }

    return (
        <Search
            loading={loading}
            value={query}
            results={results}
            onSearchChange={(e) => { setQuery(e.target.value); requestQuery(e.target.value) }}
            resultRenderer={resultRenderer}
            onResultSelect={(_, data) => { props.onChange(data.result.location); setQuery('') }}
        />
    )
}

export default Searchbar;