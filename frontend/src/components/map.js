import { VectorMap } from '@south-paw/react-vector-maps';
import World from './maps/world.json';
import styled from 'styled-components';

import axios from 'axios';

function Map(props) {

    const Mape = styled.div`
        margin: 1rem auto;
        width: 65%;

        svg {
            stroke: #000;

            // All layers are just path elements
            path {
                fill: #fff;
                cursor: pointer;
                outline: none;

                // When a layer is hovered
                &:hover {
                    fill: #b1ccf2;
                }

                // When a layer is focused.
                &:focus {
                    fill: #2d67fa;
                }
            }
        }
    `

    const onClick = ({ target }) => {
        fetchRegion(target.attributes.id.value);
    }

    const fetchRegion = async id => {

        const config = {
            method: 'post',
            url: 'http://localhost:4000/iso_location_name',
            responseType: 'json',
            data: {iso: id}
        }

        try {
            const resp = await axios(config)
            props.onChange(resp.data['location'])
        } catch (e) {
            console.log(e);
        }
    }

    return (
        <Mape>
            <VectorMap className='WorldMap' {...World} layerProps={{ onClick }} />
        </Mape>
    );
}

export default Map;