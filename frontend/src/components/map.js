import { VectorMap } from '@south-paw/react-vector-maps';
import World from './maps/world.json';
import styled from 'styled-components';

function Map() {

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

    return (

      
            <Mape>
                <VectorMap className='WorldMap' {...World} />
            </Mape>
       

    );
}

export default Map;