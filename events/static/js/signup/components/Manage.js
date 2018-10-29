import React, {Component, Fragment} from 'react';
import * as API from "../api";
import {joinTeam, leaveTeam, setTeams} from '../actions';
import keyBy from 'lodash/keyBy';
import QRCode from './QRCode';
import Teams from './Teams';
import PeopleIcon from 'mdi-material-ui/AccountMultiple';
import QrCodeIcon from 'mdi-material-ui/Qrcode';
import Tabs from "@material-ui/core/es/Tabs/Tabs";
import Tab from "@material-ui/core/es/Tab/Tab";
import withWidth, {isWidthDown, isWidthUp} from "@material-ui/core/es/withWidth/withWidth";

class Manage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedTeamId: props.currentTeamId,
      tabIndex: 0
    };

    this.handleSelectTeam = this.handleSelectTeam.bind(this);
    this.handleJoinTeam = this.handleJoinTeam.bind(this);
    this.handleLeaveTeam = this.handleLeaveTeam.bind(this);
    this.handleCreateTeam = this.handleCreateTeam.bind(this);
    this.handleUpdateTeam = this.handleUpdateTeam.bind(this);
    this.handleTabSwitch = this.handleTabSwitch.bind(this);
  }

  handleSelectTeam(id) {
    this.setState({
      selectedTeamId: id
    })
  }

  handleJoinTeam() {
    const {event, dispatcher} = this.props;
    const {selectedTeamId} = this.state;

    API.joinTeam(event.id, selectedTeamId)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(joinTeam(mappedTeams, selectedTeamId));
        });
  }

  handleLeaveTeam() {
    const {event, dispatcher} = this.props;

    API.leaveTeam(event.id)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(leaveTeam(mappedTeams));
        });
  }

  handleCreateTeam(teamName) {
    const {event, dispatcher} = this.props;

    API.createTeam(event.id, teamName)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(setTeams(mappedTeams, response.data.participant));
        });
  }

  handleUpdateTeam(teamId, team) {
    const {event, dispatcher} = this.props;

    API.updateTeam(event.id, teamId, team)
        .then(response => {
          const mappedTeams = keyBy(response.data.teams, 'id');
          dispatcher(setTeams(mappedTeams, response.data.participant));
        })
  }

  handleTabSwitch(event, value) {
    this.setState({tabIndex: value})
  }

  render() {
    const {teams, width, checkInToken, currentTeamId, isTeamLeader, participantId} = this.props;
    const {selectedTeamId, tabIndex} = this.state;

    const selectedTeam = teams[selectedTeamId];

    return (
        <Fragment>
          <QRCode value={checkInToken}/>
        </Fragment>
    )
  }
}

export default withWidth()(Manage);
