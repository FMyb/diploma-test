import {IDisposable, DisposableDelegate} from '@lumino/disposable';

import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {ToolbarButton, InputDialog} from '@jupyterlab/apputils';

import {DocumentRegistry} from '@jupyterlab/docregistry';

// import fetch from 'node-fetch';

import {NotebookPanel, INotebookModel} from '@jupyterlab/notebook';

const plugin: JupyterFrontEndPlugin<void> = {
    activate,
    id: 'toolbar-button',
    autoStart: true
};

type VM = {
    id: string;
    name: string;
};

type AvailableVMResponse = {
    data: VM[];
};

export class ButtonExtension
    implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {
    createNew(
        panel: NotebookPanel,
        context: DocumentRegistry.IContext<INotebookModel>
    ): IDisposable {
        let availableVm: AvailableVMResponse | undefined = undefined;
        const currentAddress : string = "http://158.160.25.120:8080";
        const getAvailableVm = async () => {
            const available_vm_response = await fetch(
                `${currentAddress}/api/available_vm`,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json'
                    }
                }
            );
            if (!available_vm_response.ok) {
                throw new Error(`Error! status: ${available_vm_response.status}`);
            }
            availableVm = (await available_vm_response.json()) as AvailableVMResponse;
        };
        getAvailableVm().catch(e => {
            throw e;
        });
        console.log(availableVm);
        const switchVM = async () => {
            let items: string[];
            if (availableVm != undefined) {
                items = availableVm.data.map(it => it.name);
            } else {
                items = ['current vm'];
            }
            return InputDialog.getItem({
                title: 'Switch to vm',
                items: items
            }).then(async result => {
                if (result.button.accept && availableVm != undefined) {
                    let vm = availableVm.data.find(it => it.name === result.value);
                    if (vm != undefined) {
                        const response =  await fetch(`${currentAddress}/api/switch_vm`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(vm)
                        });
                        if (!response.ok) {
                            throw new Error('failed to switch vm');
                        }
                        if (response.body == null) {
                            location.href = document.location.href
                        } else {
                            location.href = await response.text()
                        }
                    }
                }
            })
        };

        const button = new ToolbarButton({
            className: 'Move state',
            label: 'Move state',
            onClick: switchVM,
            tooltip: 'Move state'
        });

        panel.toolbar.insertItem(10, 'moveState', button);
        return new DisposableDelegate(() => {
            button.dispose();
        });
    }
}

function activate(app: JupyterFrontEnd): void {
    app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension());
}

export default plugin;